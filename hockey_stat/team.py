import logging
import typing as t
from dataclasses import dataclass, field

from bs4 import BeautifulSoup

from hockey_stat.player import Player, PlayerParser
from hockey_stat.requester import make_request

logger = logging.getLogger(__name__)


@dataclass
class TeamInfo:
    name: str
    url: str
    players: t.List[Player] = field(default_factory=list)


class TeamParser:
    def __init__(self, name: str, url: str):
        self._team = TeamInfo(name=name, url=url)

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

        players = players_wrap.find_all("a", class_="team-player-card__name")
        if not players:
            logger.warning("can not find players info data")
            return

        for item in players:
            player_url = item.attrs["href"]
            player_id = player_url.rsplit("-", 1)[1][:-1]
            if player := PlayerParser(player_id, player_url).parse():
                logger.debug("add player %s (%s)", player.name, player_id)
                self._team.players.append(player)
