import pytest


class TestUserModel:

    def test_user_matches_missing_city(self, db, user):
        user.city = None
        assert user.get_matches() == []

    def test_all_users_active(self, user):
        assert user.is_active() == True

    def test_user_id_is_netid(self, user):
        assert user.get_id() == user.netid

    def test_user_email_grad_year_missing(self, user):
        user.grad_year = None
        assert user.email == user.netid + "@dartmouth.edu"

    def test_user_send_welcome(self, worker, outbox, user):
        user.send_welcome_notification()
        worker.work(burst=True)
        assert len(outbox) == 1
        assert "Welcome" in outbox[0].subject

    def test_user_send_new_matches_wrong_gender(self, outbox, sf_user,
                                                female_sf_user):
        sf_user.send_new_matches_notifications()
        assert len(outbox) == 0
