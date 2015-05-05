import pytest
import json

from datetime import datetime

from . import TestBase


class TestUserAPI(TestBase):

    def test_get_user(self, test_client, user):
        with test_client.session_transaction() as sess:
            sess['user_id'] = user.netid

        get = test_client.get('/api/user')
        self.check_valid_header_type(get.headers)
        data = json.loads(get.data)
        assert data['user']['netid'] == user.netid

    def test_put_user(self, test_client, user):
        with test_client.session_transaction() as sess:
            sess['user_id'] = user.netid

        data = dict(nickname="Alex",
                    start_date=datetime.now().date(),
                    city="New York", grad_year=2015,
                    time_period=10)
        put = test_client.put('/api/user', data=data)
        self.check_valid_header_type(put.headers)
        data = json.loads(put.data)
        print data
        assert data['user']['nickname'] == "Alex"
        assert data['user']['netid'] == user.netid

    def test_delete_user(self, test_client, user):
        with test_client.session_transaction() as sess:
            sess['user_id'] = user.netid

        # Remove dummy user
        delete = test_client.delete('/api/user')
        self.check_valid_header_type(delete.headers)
        data = json.loads(delete.data)
        assert data['result'] == True


class TestUserMatchesAPI(TestBase):

    def test_get_user_matches(self, test_client, sf_user, sf_users):
        with test_client.session_transaction() as sess:
            sess['user_id'] = sf_user.netid

        matches = test_client.get('/api/users/matches')
        self.check_valid_header_type(matches.headers)
        data = json.loads(matches.data)
        assert len(data['users']) == 5

    def test_no_matches_from_finished_searchers(self, test_client,
                                                finished_sf_user, sf_user):
        with test_client.session_transaction() as sess:
            sess['user_id'] = sf_user.netid

        matches = test_client.get('/api/users/matches')
        self.check_valid_header_type(matches.headers)
        data = json.loads(matches.data)
        assert data['users'] == []

    def test_no_matches_outside_start_date_range(self, test_client,
                                                 old_sf_user, sf_user):
        with test_client.session_transaction() as sess:
            sess['user_id'] = sf_user.netid

        matches = test_client.get('/api/users/matches')
        self.check_valid_header_type(matches.headers)
        data = json.loads(matches.data)
        assert data['users'] == []

    def test_no_matches_outside_city(self, test_client, ny_user, sf_user):
        with test_client.session_transaction() as sess:
            sess['user_id'] = sf_user.netid

        matches = test_client.get('/api/users/matches')
        self.check_valid_header_type(matches.headers)
        data = json.loads(matches.data)
        assert data['users'] == []

    def test_get_user_matches_no_matches(self, test_client, user):
        with test_client.session_transaction() as sess:
            sess['user_id'] = user.netid

        matches = test_client.get('/api/users/matches')
        self.check_valid_header_type(matches.headers)
        data = json.loads(matches.data)
        assert data['users'] == []
