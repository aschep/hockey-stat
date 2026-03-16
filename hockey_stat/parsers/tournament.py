import logging
import typing as t
from datetime import datetime
from urllib.parse import parse_qs, urlsplit

from bs4 import BeautifulSoup

from hockey_stat.core.models import Game, Group, TeamResult, Tournament
from hockey_stat.requester import make_request

logger = logging.getLogger(__name__)


components = {
    "calendar": "itprofit:competitions-calendar",
    "tournament": "itprofit:tournament-page",
}


def _make_params(key: str, prm: str):
    return {
        "params": prm,
        "component": components[key],
    }


class TournamentParser:
    def __init__(self, name: str, url: str):
        self._name = name
        self._url = url
        self._tours: t.List[Tournament] = []

    def ages(self) -> t.List[int]:
        return [t.age for t in self._tours]

    @property
    def tournaments(self):
        return self._tours

    def parse(self):
        self._tours.clear()
        content = make_request(self._url)
        if not content:
            return

        soup = BeautifulSoup(content, "html5lib")

        select = soup.find("select", class_="select-el")
        if not select:
            logger.error("Tournament parse error: can not found `select`")
            return

        for item in select.find_all("option"):
            parsed_url = urlsplit(item["data-ajax"])
            params = parse_qs(parsed_url.query)
            tour_prm = params["params"][0]

            self._tours.append(
                Tournament(
                    name=self._name,
                    age=int(item.text.strip()),
                    url=parsed_url.path,
                    key=tour_prm,
                )
            )


class GroupsParser:
    def __init__(self, tournament: Tournament):
        self._tournament = tournament
        self.groups_ = []

    @property
    def groups(self) -> t.List[Group]:
        return self.groups_

    def parse(self) -> None:
        self.groups_.clear()
        content = make_request(self._tournament.url, _make_params("tournament", self._tournament.key))
        if not content:
            return

        soup = BeautifulSoup(content, "html5lib")
        div = soup.find("div", class_="filter-block")
        if not div:
            logger.error("groups parser error: can not found div filter-block")
            return

        for item in div.find_all("div", class_="filter-btn"):
            parsed_url = urlsplit(item["data-ajax-link"])
            key = parse_qs(parsed_url.query)["params"][0]

            games = self.parse_concrete_group(parsed_url.path, _make_params("calendar", key), self.construct_game)
            teams = self.parse_concrete_group(
                parsed_url.path,
                _make_params("tournament", key),
                self.construct_team_stats,
            )
            group = Group(
                name=item.text.strip(),
                url=parsed_url.path,
                key=key,
                teams=teams,
                games=sorted(games, key=lambda x: x.number),
            )
            self.groups_.append(group)

    @staticmethod
    def construct_team_stats(row):
        names = (
            "games",
            "wins",
            "wins_ot",
            "wins_st",
            "loss",
            "loss_ot",
            "loss_st",
            "goal_scored",
            "goal_allowed",
            "plus_minus",
            "points",
        )
        cols = row.find_all("td")
        item = cols[1]
        return TeamResult(
            place=int(cols[0].text.strip()),
            name=item.find("span", class_="team-title").text.strip(),
            city=item.find("span", class_="team-city").text.strip(),
            url=item.find("a", class_="link-tr")["href"],
            **{key: int(item.text.strip()) for key, item in zip(names, cols[2:])},
        )

    @staticmethod
    def construct_game(row):
        cols = row.find_all("td")
        date = cols[1].find("span", class_="date").text.strip()
        time = cols[1].find("span", class_="time").text.strip().split()[0]

        home_item = cols[2].find("div", class_="cell team")
        home_name = home_item.find("span", class_="team-title").text.strip()
        home_city = home_item.find("span", class_="team-city").text.strip()

        guest_item = cols[3].find("div", class_="cell team")
        guest_name = guest_item.find("span", class_="team-title").text.strip()
        guest_city = guest_item.find("span", class_="team-city").text.strip()
        return Game(
            number=int(cols[0].text.strip()),
            date=datetime.strptime(f"{date} {time}", "%d.%m.%Y %H:%M"),
            home_team=f"{home_name} {home_city}",
            guest_team=f"{guest_name} {guest_city}",
            result=cols[4].text.strip(),
            url=cols[0].find("a")["href"],
        )

    @staticmethod
    def parse_concrete_group(url_, params, constructor_) -> t.Optional[t.List[t.Union[TeamResult, Game]]]:
        content = make_request(url_, params)
        if not content:
            return

        soup = BeautifulSoup(content, "html5lib")
        table = soup.find("table", class_="table")
        if not table:
            logger.error("concrete group parse error: can not found table class. params: %%r", params)
            return

        return [constructor_(row) for row in table.find("tbody").find_all("tr")]
