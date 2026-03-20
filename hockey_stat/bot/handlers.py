from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from hockey_stat.storage.dao.team import TeamDAO
from hockey_stat.storage.dao.tournament import TournamentDAO

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    print("cmd_start")
    await message.answer(
        "ХоккейStat Bot запущен!",
        parse_mode="Markdown",
    )


@router.message(Command("tours"))
async def cmd_tour(message: Message, tour_dao: TournamentDAO):
    tours = await tour_dao.get_all()
    msg = "\n".join(f"{tour.name} {tour.age}" for tour in tours)
    await message.answer(
        f"Турниры:\n\n{msg}",
        parse_mode="Markdown",
    )


@router.message(Command("team"))
async def cmd_team(message: Message, team_dao: TeamDAO):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("❌ `/team <team name>`", parse_mode="Markdown")
        return

    name = args[1]
    team = await team_dao.get_team_by_name(name)
    if not team:
        await message.answer(f"Команда `{name}` не найдена")
        return

    msg = "\n".join(f"\t {player.number}. {player.name}: {player.position} ({player.grip})" for player in team.players)

    await message.answer(f"Игроки {name}")
    await message.answer(
        msg,
        parse_mode="Markdown",
    )
