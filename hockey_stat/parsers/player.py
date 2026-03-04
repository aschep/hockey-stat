import json
import logging
import re
import typing as t

from bs4 import BeautifulSoup

from hockey_stat.core.models import Player, PlayerGameStat
from hockey_stat.requester import make_request

logger = logging.getLogger(__name__)


class PlayerParser:
    pars_re = re.compile(r"^<div class=\"cell vert-sort\">(.*)<\/div>$")
    columns_re = {
        "score": re.compile(r"^<div class=\"cell  score\">(.*)<\/div>$"),
        "tournament": re.compile(r"^<div class=\"cell\">(.*)<\/div>$"),
        "date": re.compile(r"^<div class=\"cell date\">(.*)<\/div>$"),
        "teams": re.compile(r"^<div class=\"cell\">(.*)<\/div>$"),
    }
    stat_pars_re = re.compile(r"^<div class=\"cell cell--center\">(.*)<\/div>$")
    stat_re = {
        "score": re.compile(r"^<div class=\"cell score\">(.*)<\/div>$"),
        "tournament": re.compile(r"^<div class=\"cell\">(.*)<\/div>$"),
        "date": re.compile(r"^<div class=\"cell date\">(.*)<\/div>$"),
        "teams": re.compile(
            r"^<div class=\"cell teams\">"
            r"<a href=\"\/games\/\d+\/\?teamId=\d+-\d+\" class=\"(member)?\">(.*)<\/a>"
            r"<a href=\"\/games\/\d+\/\?teamId=\d+-\d+\" class=\"(member)?\">(.*)<\/a>"
            r"<\/div>$"
        ),
    }

    def __init__(self, player_id: str, number: int, url: str):
        self._player_id = player_id
        self.player_stats_url = f"/local/components/itprofit/player-stat/templates/.default/ajax-matches.php?player_id={player_id}"
        self._number = number
        self._url = url

    def parse(self) -> t.Optional[Player]:
        content = make_request(self._url)
        if not content:
            logger.warning("can not make player statistics request with %s", self._url)
            return

        soup = BeautifulSoup(content, "html.parser")
        player_info = soup.find("div", class_="player-header__body")
        if not player_info:
            logger.warning("can not find player info")
            return

        name = player_info.find("h2", class_="player-header__title")
        fields = {"name": name.text.strip()}
        keys = ("position", "height", "weight", "grip", "birthday", "nation", "school")
        for key, item in zip(
            keys, player_info.find_all("div", class_="player-data__row-item")
        ):
            if key == "nation":
                continue
            span = item.find_next("span")
            fields[key] = span.text.strip()

        return Player(
            player_id=self._player_id,
            player_url=self._url,
            number=self._number,
            **fields,
        )

    def parse_stats(self) -> t.List[PlayerGameStat]:
        content = make_request(self.player_stats_url)
        if not content:
            logger.warning("can not make player statistics request with %s", self._url)
            return []

        content = json.loads(content)

        columns = {}
        for item in content["columns"]:
            key = item["data"]
            columns[key] = (
                self.columns_re.get(key, self.pars_re).match(item["title"]).group(1)
            )

        stats = []
        data = content["data"][:-1]
        for item in data:
            item_stat = {}
            for key, name in columns.items():
                regx = self.stat_re.get(key, self.pars_re)
                matched = regx.match(item[key])
                if not matched:
                    break
                if key == "teams":
                    value = f"{matched[2].strip()} : {matched[4].strip()}"
                else:
                    value = matched[1].strip()
                item_stat[key] = value
            if item_stat:
                stats.append(
                    PlayerGameStat(
                        tournament=item_stat["tournament"],
                        date=item_stat["date"],
                        score=item_stat["score"],
                        teams=item_stat["teams"],
                        goals=int(item_stat["par2"]),
                        assists=int(item_stat["par3"]),
                        points=int(item_stat["par4"]),
                        plus=int(item_stat["par5"]),
                        minus=int(item_stat["par6"]),
                        plus_minus=int(item_stat["par7"]),
                    )
                )

        return stats
