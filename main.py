import argparse
import logging
import sys

from hockey_stat.parsers.team import TeamParser
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
    logger.info("parser %s", args.parser)

    if args.debug:
        handler.setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)

    if args.parser:
        team_parser = TeamParser(args.name, args.url)
        logger.debug("start parse team `%s`", team_parser.team.name)
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


if __name__ == "__main__":
    main()
