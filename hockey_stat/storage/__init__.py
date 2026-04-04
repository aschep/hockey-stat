import logging
import typing as t

from hockey_stat.core.models import Group, TeamInfo, Tournament

from .database import SessionLocal
from .repository import (
    GameRepository,
    GroupRepository,
    TeamGroupStatsRepository,
    TeamRepository,
    TournamentRepository,
)

logger = logging.getLogger(__name__)


def save_teams_and_stats(db_session, group: Group, db_group_id: int) -> t.Dict[str, int]:
    stat_repo = TeamGroupStatsRepository(db_session)
    team_repo = TeamRepository(db_session)
    team_ids: t.Dict[str, int] = {}
    for team in group.teams:
        team_info = TeamInfo(name=team.name, city=team.city, url=team.url)
        db_team = team_repo.save(team_info)
        team_ids[db_team.name] = db_team.id

        stat_repo.save(team, db_group_id)

    return team_ids


def save_games(db_session, group: Group, db_group_id: int, team_ids: t.Dict[str, int]) -> int:
    game_repo = GameRepository(db_session)
    game_counter = 0
    for game in group.games:
        home_id = team_ids[game.home_team]
        guest_id = team_ids[game.guest_team]
        game_repo.save(game, db_group_id, home_id, guest_id)
        game_counter += 1
    return game_counter


def save_tournaments(tournaments: t.List[Tournament]):
    logger.info("Start saving tournaments to db")
    with SessionLocal() as db_session:
        tour_repo = TournamentRepository(db_session)
        group_repo = GroupRepository(db_session)

        group_counter = 0
        game_counter = 0

        for tour in tournaments:
            db_tour = tour_repo.save(tour)

            for group in tour.groups:
                db_group = group_repo.save(group, db_tour.id)
                group_counter += 1

                team_ids = save_teams_and_stats(db_session, group, db_group.id)

                game_counter += save_games(
                    db_session,
                    group,
                    db_group.id,
                    team_ids,
                )

        db_session.commit()
        logger.info(
            "Saved %d tournaments, %d groups, %d games",
            len(tournaments),
            group_counter,
            game_counter,
        )
