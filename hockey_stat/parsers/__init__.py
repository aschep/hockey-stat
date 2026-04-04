import logging
import typing as t

from hockey_stat.core.models import Tournament

from .tournament import GroupsParser, TournamentParser

logger = logging.getLogger(__name__)


def parse_tournaments_and_groups(tournament_name: str, tournament_url: str) -> t.List[Tournament]:
    tour_parser = TournamentParser(tournament_name, tournament_url)
    logger.info("parsing tournament `%s`", tournament_name)
    tour_parser.parse()
    logger.info("parsed tournaments for ages %r", tour_parser.ages())

    for tour in tour_parser.tournaments:
        logger.info("parsing calendar and standings for '%s %d'", tour.name, tour.age)
        groups_parser = GroupsParser(tour)
        groups_parser.parse()
        tour.groups = groups_parser.groups
        logger.info("parsed %d groups: %r", len(tour.groups), tuple(g.name for g in tour.groups))

    return tour_parser.tournaments
