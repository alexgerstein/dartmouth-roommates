import pytest


class TestUserModel():

    def test_user_matches_missing_city(self, db, user):
        user.city = None
        assert user.get_roommate_matches() == []

    def test_all_users_active(self, user):
        assert user.is_active() == True

    def test_user_id_is_netid(self, user):
        assert user.get_id() == user.netid
