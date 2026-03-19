from hockey_stat.core.models import Group
from hockey_stat.storage.repository import GroupRepository


class TestGroupRepository:
    @staticmethod
    def check_group(result, expected, tid):
        assert result.tournament_id == tid
        assert result.name == expected.name
        assert result.url == expected.url
        assert result.key == expected.key

    def test_group_save(self, get_db, tournament_db, group):
        saved = GroupRepository(get_db).save(group, tournament_db.id)
        self.check_group(saved, group, tournament_db.id)

    def test_group_find(self, get_db, tournament_db, group_db):
        found = GroupRepository(get_db).find_by_name_tournament_id(tournament_db.id, group_db.name)
        self.check_group(found, group_db, tournament_db.id)

    def test_group_update(self, get_db, tournament_db, group_db):
        group1 = Group(name="super group", url="poper url", key="poper key")
        saved1 = GroupRepository(get_db).save(group1, tournament_db.id)

        self.check_group(saved1, group1, tournament_db.id)
        assert saved1.name == group_db.name
        assert saved1.tournament_id == tournament_db.id
