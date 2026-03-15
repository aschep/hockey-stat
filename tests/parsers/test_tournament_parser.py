import datetime

from conftest import read_file
from hockey_stat.core.models import Tournament
from hockey_stat.parsers.tournament import GroupsParser, TournamentParser


def test_parser_player_info(monkeypatch):
    monkeypatch.setattr("hockey_stat.parsers.tournament.make_request", read_file)

    tour_parser = TournamentParser("blabla tour", "tests/data/tournament_info.html")
    tour_parser.parse()
    ages = tour_parser.ages()

    assert ages == [2012, 2013, 2014]

    tour = tour_parser.tournaments[0]
    assert tour.name == "blabla tour"
    assert tour.age == 2012
    assert tour.url == "/fhr-ajax/SXRwcm9maXRcQXBwXEFqYXhcQWpheENvbXBvbmVudA==/cmVuZGVyQ29tcG9uZW50/"
    assert (
        tour.key
        == "YTo0OntzOjEzOiJUT1VSTkFNRU5UX0lEIjtzOjg6IjE2NzM1MDkyIjtzOjg6IkdST1VQX0lEIjtOO3M6NzoiWUVBUl9JRCI7czo4OiIxNjc2NzQxNiI7czo3OiJpc19hamF4IjtiOjE7fQ=="
    )

    tour = tour_parser.tournaments[1]
    assert tour.name == "blabla tour"
    assert tour.age == 2013
    assert tour.url == "/fhr-ajax/SXRwcm9maXRcQXBwXEFqYXhcQWpheENvbXBvbmVudA==/cmVuZGVyQ29tcG9uZW50/"
    assert (
        tour.key
        == "YTo0OntzOjEzOiJUT1VSTkFNRU5UX0lEIjtzOjg6IjE2NzM1MDkyIjtzOjg6IkdST1VQX0lEIjtOO3M6NzoiWUVBUl9JRCI7czo4OiIxNjc2NzQxOCI7czo3OiJpc19hamF4IjtiOjE7fQ=="
    )

    tour = tour_parser.tournaments[2]
    assert tour.name == "blabla tour"
    assert tour.age == 2014
    assert tour.url == "/fhr-ajax/SXRwcm9maXRcQXBwXEFqYXhcQWpheENvbXBvbmVudA==/cmVuZGVyQ29tcG9uZW50/"
    assert (
        tour.key
        == "YTo0OntzOjEzOiJUT1VSTkFNRU5UX0lEIjtzOjg6IjE2NzM1MDkyIjtzOjg6IkdST1VQX0lEIjtOO3M6NzoiWUVBUl9JRCI7czo4OiIxNjc2NzQxOSI7czo3OiJpc19hamF4IjtiOjE7fQ=="
    )


def test_groups_parser_parse(monkeypatch):
    def _mock(_, __, ___):
        return []

    monkeypatch.setattr("hockey_stat.parsers.tournament.make_request", read_file)

    tournament = Tournament(
        name="blabla name",
        age=2013,
        url="tests/data/groups_info.html",
        key="YTo0OntzOjEzOiJUT1VSTkFNRU5UX0lEIjtzOjg6IjE2NzM1MDkyIjtzOjg6IkdST1VQX0lEIjtOO3M6NzoiWUVBUl9JRCI7czo4OiIxNjc2NzQxOCI7czo3OiJpc19hamF4IjtiOjE7fQ",
    )

    groups_parser = GroupsParser(tournament)
    groups_parser.parse_concrete_group = _mock
    groups_parser.parse()

    assert len(groups_parser.groups) == 3

    g = groups_parser.groups[0]
    assert g.name == "Группа А1"
    assert g.url == "/fhr-ajax/SXRwcm9maXRcQXBwXEFqYXhcQWpheENvbXBvbmVudA==/cmVuZGVyQ29tcG9uZW50/"
    assert (
        g.key
        == "YTo0OntzOjEzOiJUT1VSTkFNRU5UX0lEIjtzOjg6IjE2NzM1MDkyIjtzOjg6IkdST1VQX0lEIjtzOjg6IjE3MTkzNzY0IjtzOjc6IllFQVJfSUQiO3M6ODoiMTY3Njc0MTYiO3M6NzoiaXNfYWpheCI7YjoxO30="
    )

    g = groups_parser.groups[1]
    assert g.name == "Группа А2"
    assert g.url == "/fhr-ajax/SXRwcm9maXRcQXBwXEFqYXhcQWpheENvbXBvbmVudA==/cmVuZGVyQ29tcG9uZW50/"
    assert (
        g.key
        == "YTo0OntzOjEzOiJUT1VSTkFNRU5UX0lEIjtzOjg6IjE2NzM1MDkyIjtzOjg6IkdST1VQX0lEIjtzOjg6IjE2NzcyMjEwIjtzOjc6IllFQVJfSUQiO3M6ODoiMTY3Njc0MTYiO3M6NzoiaXNfYWpheCI7YjoxO30="
    )

    g = groups_parser.groups[2]
    assert g.name == "Группа Б1"
    assert g.url == "/fhr-ajax/SXRwcm9maXRcQXBwXEFqYXhcQWpheENvbXBvbmVudA==/cmVuZGVyQ29tcG9uZW50/"
    assert (
        g.key
        == "YTo0OntzOjEzOiJUT1VSTkFNRU5UX0lEIjtzOjg6IjE2NzM1MDkyIjtzOjg6IkdST1VQX0lEIjtzOjg6IjE3MTk0MTkyIjtzOjc6IllFQVJfSUQiO3M6ODoiMTY3Njc0MTYiO3M6NzoiaXNfYWpheCI7YjoxO30="
    )


def test_groups_parser_concrete_group_calendar(monkeypatch):
    monkeypatch.setattr("hockey_stat.parsers.tournament.make_request", read_file)

    games = GroupsParser.parse_concrete_group("tests/data/calendar_info.html", {}, GroupsParser.construct_game)

    assert len(games) == 2

    g = games[0]
    assert g.number == 59
    assert g.date == datetime.datetime(year=2025, month=12, day=21, hour=9, minute=45)
    assert g.home_team == "Команда 1 Город 1"
    assert g.guest_team == "Команда 2 Город 2"
    assert g.result == "0:19"
    assert g.url == "/games/17392283/"

    g = games[1]
    assert g.number == 58
    assert g.date == datetime.datetime(year=2025, month=12, day=21, hour=8, minute=00)
    assert g.home_team == "Команда 3 Город 3"
    assert g.guest_team == "Команда 4 Город 4"
    assert g.result == "8:6"
    assert g.url == "/games/17392282/"


def test_groups_parser_concrete_group_teams(monkeypatch):
    monkeypatch.setattr("hockey_stat.parsers.tournament.make_request", read_file)

    teams = GroupsParser.parse_concrete_group("tests/data/team_stats.html", {}, GroupsParser.construct_team_stats)

    assert len(teams) == 2

    t = teams[0]
    assert t.place == 1
    assert t.name == "Команда 1"
    assert t.city == "Город 1"
    assert t.games == 20
    assert t.wins == 20
    assert t.wins_ot == 0
    assert t.wins_st == 0
    assert t.loss == 0
    assert t.loss_ot == 0
    assert t.loss_st == 0
    assert t.goal_scored == 231
    assert t.goal_allowed == 19
    assert t.plus_minus == 212
    assert t.points == 40
    assert t.url == "team_7578199/"

    t = teams[1]
    assert t.place == 2
    assert t.name == "Команда 2"
    assert t.city == "Город 2"
    assert t.games == 20
    assert t.wins == 15
    assert t.wins_ot == 0
    assert t.wins_st == 0
    assert t.loss == 0
    assert t.loss_ot == 0
    assert t.loss_st == 5
    assert t.goal_scored == 110
    assert t.goal_allowed == 69
    assert t.plus_minus == 41
    assert t.points == 30
    assert t.url == "team_7483692/"
