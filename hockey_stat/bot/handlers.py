import logging
import typing as t

from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    ReplyKeyboardRemove,
)

from hockey_stat.storage.dao.team import TeamDAO
from hockey_stat.storage.dao.tournament import GroupDAO, TournamentDAO

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
router = Router()


def make_row_keyboard(
    items: t.Sequence[t.Union[str, int]], items_in_row=4, show_back=False, show_reset=True
) -> InlineKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :param items_in_row: количество кнопок в одно ряду
    :param show_back: показывать кнопку `Назад`
    :param show_reset: показывать кнопку `Сброс`
    :return: объект реплай-клавиатуры
    """
    rows = []
    row = []
    for item in items:
        row.append(InlineKeyboardButton(text=item, callback_data=item))
        if len(row) == items_in_row:
            rows.append(row.copy())
            row.clear()

    if row:
        rows.append(row.copy())
        row.clear()

    if show_back:
        row.append(InlineKeyboardButton(text="Назад", callback_data="back"))

    if show_reset:
        row.append(InlineKeyboardButton(text="Сброс", callback_data="reset"))

    if row:
        rows.append(row)

    return InlineKeyboardMarkup(inline_keyboard=rows)


class TournamentState(StatesGroup):
    tournament_name = State()
    tournament_age = State()
    group_name = State()
    entity = State()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()

    msg = "Bot запущен!\n" "/tour - информация о текущем турнире"
    await message.answer(msg, reply_markup=ReplyKeyboardRemove())


@router.callback_query(F.data == "reset")
async def reset_state(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("/tour - информация о текущем турнире")
    await callback.answer()


@router.message(StateFilter("*"), Command("back"))
async def reset_state(message: Message, state: FSMContext):
    if state.get_state() == TournamentState.tournament_name:
        await state.clear()
        await message.answer("/tour - информация о текущем турнире")


@router.message(StateFilter(None), Command("tour"))
async def cmd_tour_start(message: Message, state: FSMContext, tour_dao: TournamentDAO):
    """
    Начальная точка FSM. спрашиваем имя турнира
    :param message:
    :param state:
    :param tour_dao: объект для получения данных о турнире из БД
    :return: None
    """
    tour_names = await tour_dao.get_names()
    if not tour_names:
        await message.answer(text="Нет ни одного турнира")
        return

    logger.info("tournaments found: %r", tour_names)
    await message.answer(text="Выберите турнир:", reply_markup=make_row_keyboard(tour_names, show_back=False))
    await state.set_state(TournamentState.tournament_name)


@router.callback_query(StateFilter(TournamentState.tournament_name))
async def cmd_set_tour_name(callback: CallbackQuery, state: FSMContext, tour_dao: TournamentDAO):
    """
    Получаем имя турнира. Спрашиваем возраст.
    :param callback: имя турнира
    :param state:
    :param tour_dao: объект для получения данных о турнире из БД
    :return: None
    """
    logger.info("get tournament %s", callback.data)
    await state.update_data(tournament_name=callback.data)
    tour_ages = await tour_dao.get_ages(callback.data)
    if not tour_ages:
        await callback.message.answer(text=f"Нет ни одного возраста для турнира {callback.data}")
        return

    logger.info("tournament ages found: %r", tour_ages)
    await callback.message.answer(
        text="Выберите возраст:", reply_markup=make_row_keyboard([f"{age}" for age in tour_ages])
    )
    await state.set_state(TournamentState.tournament_age)
    await callback.answer()


@router.callback_query(StateFilter(TournamentState.tournament_age))
async def cmd_set_tour_age(callback: CallbackQuery, state: FSMContext, tour_dao: TournamentDAO, group_dao: GroupDAO):
    """
    Получили возраст. Получаем id конкретного турнира. Спрашиваем группу.
    :param callback: возраст
    :param state:
    :param tour_dao: объект для получения данных о турнире из БД
    :param group_dao: объект для получения данных о группах из БД
    :return:
    """
    tour_data = await state.get_data()
    tour_name = tour_data["tournament_name"]
    tour_age = int(callback.data)
    tour_id = await tour_dao.get_id(tour_name, tour_age)
    if not tour_id:
        await callback.message.answer(text=f"Не могу найти турнир {tour_name} ({tour_age})")
        await callback.answer()
        return
    await state.update_data(tournament_age=tour_age, tournament_id=tour_id)

    tour_groups = await group_dao.get_group_names(tour_id)
    if not tour_groups:
        await callback.message.answer(text=f"Не могу найти группы для турнира {tour_name} ({tour_age})")
        return

    logger.info("tournament groups found: %r", tour_groups)
    await callback.message.answer(text="Что показать:", reply_markup=make_row_keyboard(tour_groups))
    await state.set_state(TournamentState.group_name)
    await callback.answer()


entities = ["Таблица", "Календарь"]


@router.callback_query(StateFilter(TournamentState.group_name))
async def cmd_set_group_name(callback: CallbackQuery, state: FSMContext):
    """
    Получили группу в турнире. Что выводим: таблицу или календарь?
    :param callback: имя группы
    :param state:
    :param group_dao: объект для получения данных о группах из БД
    :return: None
    """
    tour_data = await state.get_data()
    group_name = tour_data["group_name"] if "group_name" in tour_data else callback.data

    await state.update_data(group_name=group_name)

    await callback.message.answer(text="Что показать:", reply_markup=make_row_keyboard(entities))
    await state.set_state(TournamentState.entity)
    await callback.answer()


@router.callback_query(StateFilter(TournamentState.entity), F.data.in_(entities))
async def cmd_set_group_name(callback: CallbackQuery, state: FSMContext, group_dao: GroupDAO):
    tour_data = await state.get_data()
    logger.info("Tour data %r", tour_data)
    tour_id = tour_data["tournament_id"]
    group_name = tour_data["group_name"]

    msg = f"{callback.data} - это что еще такое?!"
    if callback.data == entities[1]:  # календарь
        games = await group_dao.get_group_calendar(name=group_name, tour_id=tour_id)
        if games:
            lines = ["Следующие 10 игр в сезоне"]

            for game in games:
                date_str = game.date.strftime("%d.%m %H:%M")
                home = (game.home_team.name + "        ")[:18]
                guest = (game.guest_team.name + "        ")[:18]
                lines.append(f"{date_str:<12}: {home} vs {guest}")
        else:
            lines = ["В этой группе все игры сыграны."]

        msg = "<pre>" + "\n".join(lines) + "</pre>"

    elif callback.data == entities[0]:  # таблица
        teams = await group_dao.get_group_table(name=group_name, tour_id=tour_id)
        lines = ["№ Команда: Очки (Игры)"]

        for team_stat in teams:
            place = f"{team_stat.place:>4}"
            name = f"{team_stat.team.name:<18}"
            games_str = f"{team_stat.games:>4}"
            points = f"{team_stat.points:>4}"
            lines.append(f"{place}. {name}: {points} ({games_str})")

        msg = "<pre>" + "\n".join(lines) + "</pre>"

    await callback.message.answer(msg, parse_mode=ParseMode.HTML)
    await callback.message.answer(text="Что показать:", reply_markup=make_row_keyboard(entities))
    await callback.answer()


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
