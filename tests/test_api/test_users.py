import pytest
import json

from . import TestBase


class TestUserAPI(TestBase):

    def test_delete_user(self, test_client, user):
        with test_client.session_transaction() as sess:
            sess['user_id'] = user.netid

        # Remove dummy user
        delete = test_client.delete('/api/user')
        self.check_valid_header_type(delete.headers)
        data = json.loads(delete.data)
        assert data['result'] == True


class TestUserMatchesAPI(TestBase):

    def test_get_user_matches_no_matches(self, test_client, user):
        with test_client.session_transaction() as sess:
            sess['user_id'] = user.netid

        matches = test_client.get('/api/users/matches')
        self.check_valid_header_type(matches.headers)
        data = json.loads(matches.data)
        assert data['users'] == []
