import argparse
import logging
import sys
import typing as t

from hockey_stat.core.models import TeamInfo
from hockey_stat.parsers.team import TeamParser
from hockey_stat.parsers.tournament import GroupsParser, TournamentParser
from hockey_stat.storage.database import SessionLocal
from hockey_stat.storage.repository import (
    GameRepository,
    GroupRepository,
    PlayerRepository,
    TeamGroupStatsRepository,
    TeamRepository,
    TournamentRepository,
)

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
        tour_parser = TournamentParser(args.name, args.url)
        logger.info("parsing team `%s`", args.name)
        tour_parser.parse()
        logger.info("parsed tours for ages %r", tour_parser.ages())
        tournaments = tour_parser.tournaments
        for tour in tournaments:
            logger.info("parsing calendar and table for '%s %d'", tour.name, tour.age)
            groups_parser = GroupsParser(tour)
            groups_parser.parse()
            tour.groups = groups_parser.groups
            logger.info("parsed %d groups: %r", len(tour.groups), tuple(g.name for g in tour.groups))

        logger.info("start saving to db...")
        with SessionLocal() as db_session:
            team_repo = TeamRepository(db_session)
            tour_repo = TournamentRepository(db_session)
            group_repo = GroupRepository(db_session)
            game_repo = GameRepository(db_session)
            stat_repo = TeamGroupStatsRepository(db_session)

            group_counter = 0
            game_counter = 0
            for tour in tournaments:
                db_tour = tour_repo.save(tour)
                for group in tour.groups:
                    db_group = group_repo.save(group, db_tour.id)
                    group_counter += 1
                    team_ids: t.Dict[str, int] = {}
                    for team in group.teams:
                        team_info = TeamInfo(name=team.name, city=team.city, url=team.url)
                        db_team = team_repo.save(team_info)
                        team_ids[db_team.name] = db_team.id

                        stat_repo.save(team, db_group.id)

                    for game in group.games:
                        home_id = team_ids[game.home_team]
                        guest_id = team_ids[game.guest_team]
                        game_repo.save(game, db_group.id, home_id, guest_id)
                        game_counter += 1

            db_session.commit()
            logger.info("Saved %d tournaments, %d groups, %d games", len(tournaments), group_counter, game_counter)
    else:
        logger.error("you can not get here. never.")
        exit(1)


if __name__ == "__main__":
    main()
