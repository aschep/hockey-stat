import json
import logging
import re
import typing as t
from dataclasses import dataclass

from bs4 import BeautifulSoup

from hockey_stat.requester import make_request

logger = logging.getLogger(__name__)


@dataclass
class PlayerGameStat:
    tournament: str
    date: str
    score: str
    teams: str
    goals: int
    assists: int
    points: int
    plus: int
    minus: int
    plus_minus: int


@dataclass
class Player:
    name: str
    birthday: str
    position: str
    grip: str
    weight: str
    height: str
    school: str
    in_school_from: str


class PlayerParser:
    pars_re = re.compile(r"^<div class=\"cell vert-sort\">(.*)<\/div>$")
    columns_re = {
        "score": re.compile(r"^<div class=\"cell  score\">(.*)<\/div>$"),
        "tournament": re.compile(r"^<div class=\"cell\">(.*)<\/div>$"),
        "date": re.compile(r"^<div class=\"cell date\">(.*)<\/div>$"),
        "teams": re.compile(r"^<div class=\"cell\">(.*)<\/div>$")
    }
    stat_pars_re = re.compile(r"^<div class=\"cell cell--center\">(.*)<\/div>$")
    stat_re = {
        "score": re.compile(r"^<div class=\"cell score\">(.*)<\/div>$"),
        "tournament": re.compile(r"^<div class=\"cell\">(.*)<\/div>$"),
        "date": re.compile(r"^<div class=\"cell date\">(.*)<\/div>$"),
        "teams": re.compile(r"^<div class=\"cell teams\">"
                            r"<a href=\"\/games\/\d+\/\?teamId=\d+-\d+\" class=\"(member)?\">(.*)<\/a>"
                            r"<a href=\"\/games\/\d+\/\?teamId=\d+-\d+\" class=\"(member)?\">(.*)<\/a>"
                            r"<\/div>$")
    }

    def __init__(self, player_id: str, url: str):
        self._url = url
        self._player_id = player_id
        self.player_stats_url = f"local/components/itprofit/player-stat/templates/.default/ajax-matches.php?player_id={player_id}"

    def parse(self) -> t.Optional[Player]:
        content = make_request(self._url)
        if not content:
            logger.warning("can not make player statistics request with %s", self._url)
            return

        soup = BeautifulSoup(content, "html.parser")
        single_info = soup.find("div", class_="player-single__info")
        if not single_info:
            logger.warning("can not find player single info div")
            return

        data = single_info.find_all("div", class_="info__data-text")
        if not data:
            logger.warning("can not find player info data")
            return

        player_fields = (
            "name",
            "birthday",
            "school",
            "in_school_from",
            "position",
            "height",
            "weight",
            "grip",
        )
        fields = {key: item.text.strip() for key, item in zip(player_fields, data)}
        return Player(**fields)

    def parse_stats(self) -> t.List[PlayerGameStat]:
        content = make_request(self.player_stats_url)
        if not content:
            logger.warning("can not make player statistics request with %s", self._url)
            return []

        content = json.loads(content)

        columns = {}
        for item in content["columns"]:
            key = item["data"]
            columns[key] = self.columns_re.get(key, self.pars_re).match(item["title"]).group(1)

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
                    value = f"{matched[2]} : {matched[4]}"
                else:
                    value = matched[1]
                item_stat[key] = value
            if item_stat:
                stats.append(PlayerGameStat(
                    tournament=item_stat["tournament"],
                    date=item_stat["date"],
                    score=item_stat["score"],
                    teams=item_stat["teams"],
                    goals=int(item_stat["par2"]),
                    assists=item_stat["par3"],
                    points=item_stat["par4"],
                    plus=item_stat["par5"],
                    minus=item_stat["par6"],
                    plus_minus=item_stat["par7"],
                ))

        return stats
