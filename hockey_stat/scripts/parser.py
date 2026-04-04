import argparse
import logging
import sys

from hockey_stat.parsers import parse_tournaments_and_groups
from hockey_stat.parsers.team import TeamParser
from hockey_stat.storage import save_tournaments
from hockey_stat.storage.database import SessionLocal
from hockey_stat.storage.repository import PlayerRepository, TeamRepository

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(stream=sys.stdout)
handler.setLevel(logging.INFO)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action="store_true", help="show version")
    parser.add_argument("--debug", action="store_true", help="debug logging")

    subparsers = parser.add_subparsers(dest="parser", help="parser type")

    team_parser = subparsers.add_parser("team", help="parse team")
    team_parser.add_argument("name", type=str, help="team name")
    team_parser.add_argument("url", type=str, help="team url to parse")

    tournament_parser = subparsers.add_parser("tour", help="parse tournament")
    tournament_parser.add_argument("name", type=str, help="tournament name")
    tournament_parser.add_argument("url", type=str, help="tournament url to parse")

    args = parser.parse_args()
    if args.version:
        logger.info("show version")
        exit(0)

    if not args.parser:
        parser.print_help()
        exit(0)

    return args


def main():
    args = parse_args()
    logger.debug("parser %s", args.parser)

    if args.debug:
        handler.setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)

    if args.parser == "team":
        team_parser = TeamParser(args.name, args.url)
        logger.info("parsing team `%s`", team_parser.team.name)
        team_parser.parse()

        with SessionLocal() as db_session:
            team_repo = TeamRepository(db_session)
            team = team_repo.save(team_parser.team)
            db_session.commit()

            logger.debug("parsed team `%s`, store with id `%s`", team.name, team.id)

            player_repo = PlayerRepository(db_session)
            for player in team_parser.team.players:
                logger.debug("store player `%s`", player.name)
                player_repo.save(player, team.id)
            db_session.commit()
    elif args.parser == "tour":
        tournaments = parse_tournaments_and_groups(args.name, args.url)
        save_tournaments(tournaments)
    else:
        logger.error("you can not get here. never.")
        exit(1)


if __name__ == "__main__":
    main()
