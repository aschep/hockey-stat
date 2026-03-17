import logging

from bs4 import BeautifulSoup

from hockey_stat.core.models import TeamInfo
from hockey_stat.helpers import get_id_from_url
from hockey_stat.parsers.player import PlayerParser
from hockey_stat.requester import make_request

logger = logging.getLogger(__name__)


class TeamParser:
    def __init__(self, name: str, url: str):
        self._team = TeamInfo(name=name, city="", url=url)

    @property
    def team(self):
        return self._team

    def parse(self):
        content = make_request(self._team.url)
        if not content:
            logger.warning("can not make team info request with %s", self._team.url)
            return

        soup = BeautifulSoup(content, "html.parser")
        players_wrap = soup.find("div", class_="player-cards-wrap")
        if not players_wrap:
            logger.warning("can not find players info div")
            return

        players = players_wrap.find_all("div", class_="team-player-card")
        if not players:
            logger.warning("can not find players info data")
            return

        for item in players:
            number = item.find_next("span", class_="team-player-card__number").text.strip()
            link = item.find_next("a", class_="team-player-card__name")
            player_url = link.attrs["href"]
            player_id = get_id_from_url(player_url)
            if player := PlayerParser(player_id, int(number), player_url).parse():
                logger.debug("add player %s (%s)", player.name, player_id)
                self._team.players.append(player)
