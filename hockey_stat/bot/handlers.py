import logging
import typing as t

from aiogram import F, Router
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

from hockey_stat.storage.dao.team import TeamDAO
from hockey_stat.storage.dao.tournament import GroupDAO, TournamentDAO

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
router = Router()


def make_row_keyboard(items: t.Sequence[t.Union[str, int]]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


class TournamentState(StatesGroup):
    tournament_name = State()
    tournament_age = State()
    group_name = State()
    entity = State()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Bot запущен!")


@router.message(StateFilter(None), Command("tour"))
async def cmd_tour_start(message: Message, state: FSMContext, tour_dao: TournamentDAO):
    """
    Начальная точка FSM. спрашиваем имя турнира
    :param message:
    :param state:
    :param tour_dao: объект для получения данных о турнире из БД
    :return: None
    """
    tour_names = tour_dao.get_names()
    if not tour_names:
        await message.answer(text="Нет ни одного турнира")
        return

    await message.answer(text="Выберите турнир:", reply_markup=make_row_keyboard(tour_names))
    await state.set_state(TournamentState.tournament_name)


@router.message(StateFilter(TournamentState.tournament_name))
async def cmd_set_tour_name(message: Message, state: FSMContext, tour_dao: TournamentDAO):
    """
    Получаем имя турнира. Спрашиваем возраст.
    :param message: имя турнира
    :param state:
    :param tour_dao: объект для получения данных о турнире из БД
    :return: None
    """
    await state.update_data(tournament_name=message.text)
    tour_ages = tour_dao.get_ages(message.text)
    if not tour_ages:
        await message.answer(text=f"Нет ни одного возраста для турнира {message.text}")
        return

    await message.answer(text="Выберите возраст:", reply_markup=make_row_keyboard(tour_ages))
    await state.set_state(TournamentState.tournament_age)


@router.message(StateFilter(TournamentState.tournament_age))
async def cmd_set_tour_age(message: Message, state: FSMContext, tour_dao: TournamentDAO, group_dao: GroupDAO):
    """
    Получили возраст. Получаем id конкретного турнира. Спрашиваем группу.
    :param message: возраст
    :param state:
    :param tour_dao: объект для получения данных о турнире из БД
    :param group_dao: объект для получения данных о группах из БД
    :return:
    """
    tour_data = await state.get_data()
    tour_name = tour_data["tournament_name"]
    tour_age = int(message.text)
    tour_id = tour_dao.get_id(tour_name, tour_age)
    if not tour_id:
        await message.answer(text=f"Не могу найти турнир {tour_name} ({tour_age})")
        return
    await state.update_data(tournament_age=tour_age, tour_id=tour_id)

    tour_groups = group_dao.get_group_names(tour_id)
    if not tour_groups:
        await message.answer(text=f"Не могу найти группы для турнира {tour_name} ({tour_age})")
        return

    await message.answer(text="Что показать:", reply_markup=make_row_keyboard(tour_groups))
    await state.set_state(TournamentState.group_name)


entities = ["Таблица", "Календарь"]


@router.message(StateFilter(TournamentState.group_name))
async def cmd_set_group_name(message: Message, state: FSMContext, group_dao: GroupDAO):
    """
    Получили группу в турнире. Что выводим: таблицу или календарь?
    :param message: имя группы
    :param state:
    :param group_dao: объект для получения данных о группах из БД
    :return: None
    """
    tour_data = await state.get_data()
    group_name = tour_data["group_name"] if "group_name" in tour_data else message.text

    await state.update_data(group_name=group_name)

    await message.answer(text="Что показать:", reply_markup=make_row_keyboard(entities))
    await state.set_state(TournamentState.entity)


@router.message(StateFilter(TournamentState.entity), F.text.in_(entities))
async def cmd_set_group_name(message: Message, state: FSMContext, group_dao: GroupDAO):
    tour_data = await state.get_data()
    tour_id = tour_data["tournament_id"]
    group_name = tour_data["group_name"]

    msg = ""
    if message.text == entities[0]:  # календарь
        group = await group_dao.get_group_calendar(name=group_name, tour_id=tour_id)
        msg = "\n|Дата|Хозяева|Гости|Счет|\n|:---|:---:|:---:|:---:|"
        msg += "\n".join(
            f"|{game.date}|{game.home_team.name}|{game.guest_team.name}|{game.result}|" for game in group.games
        )
    elif message.text == entities[1]:  # Таблица
        group = await group_dao.get_group_table(name=group_name, tour_id=tour_id)
        msg = "\n|#|Команда|Игры|Очки|\n|:---|:---:|---:|---:|\n"
        msg += "\n".join(f"|{team.place}|{team.name}|{team.games}|{team.points}|" for team in group.teams)

    else:
        msg = f"{message.tex} - это что еще такое?!"

    await message.answer(text=msg, reply_markup=make_row_keyboard(entities))
    await state.set_state(TournamentState.group_name)


@router.message(Command("tours"))
async def cmd_tours(message: Message, tour_dao: TournamentDAO):
    tours = await tour_dao.get_all()
    msg = "\n".join(f"{tour.name} {tour.age}" for tour in tours)
    logger.debug("Tours: %s", msg)
    await message.answer(f"Турниры:\n\n{msg}")


@router.message(Command("groups"))
async def cmd_groups(message: Message, command: CommandObject, tour_dao: TournamentDAO):
    name, age = command.args.rsplit(" ", maxsplit=1)
    age = int(age)
    logger.debug("get tournament groups for %s (%d)", name, age)
    tour = await tour_dao.get_with_groups(name, age)
    if not tour:
        await message.answer(f"Отсутствуют данные по турниру {name} ({age})")
        logger.warning("can not get info for tournament %s (%d)", name, age)
        return
    logger.debug("get data for tour %s %d, amount of groups %d", tour.name, tour.age, len(tour.groups))
    msg = "\n".join(f"{group.name}" for group in tour.groups)
    await message.answer(f"Группы `{name} ({age})`:\n\n{msg}")
    logger.debug("Groups: \n%s", msg)


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
