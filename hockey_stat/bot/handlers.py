from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from hockey_stat.storage.dao.team import TeamDAO

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "🏒 **Хоккейная статистика**\n\n" "/team <name> — Состав команды\n",
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

    msg = "\n".join(
        f"\t {player.number}. {player.name}: {player.position} ({player.grip})"
        for player in team.players
    )

    await message.answer(f"Игроки {name}")
    await message.answer(
        msg,
        parse_mode="Markdown",
    )
