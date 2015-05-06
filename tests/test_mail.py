import pytest
from lodjers import mail


class TestHomePage:

    def test_welcome_notification(self, outbox, user):
        mail.welcome_notification(user)
        assert len(outbox) == 1
        assert "Welcome" in outbox[0].subject

    def test_new_matches_notification(self, outbox, user, sf_user):
        mail.new_matches_notification(user, sf_user)
        assert len(outbox) == 1
        assert "new potential roommate matches" in outbox[0].subject
