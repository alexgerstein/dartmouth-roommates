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

    def test_get_user_missing_last_visited(self, test_client, user):
        with test_client.session_transaction() as sess:
            sess['user_id'] = user.netid

        user.last_visited = None

        get = test_client.get('/api/user')
        self.check_valid_header_type(get.headers)
        data = json.loads(get.data)
        assert data['user']['netid'] == user.netid
        assert data['user']['new'] == True

    def test_put_user(self, test_client, user):
        with test_client.session_transaction() as sess:
            sess['user_id'] = user.netid

        data = dict(nickname="Alex",
                    start_date=datetime.now().date(),
                    city="New York", grad_year=2015,
                    time_period=10, searching=True)
        put = test_client.put('/api/user', data=data)
        self.check_valid_header_type(put.headers)
        data = json.loads(put.data)
        assert data['user']['nickname'] == "Alex"
        assert data['user']['netid'] == user.netid

    def test_put_user_city_abbreviation(self, test_client, user):
        with test_client.session_transaction() as sess:
            sess['user_id'] = user.netid

        data = dict(nickname="Alex",
                    start_date=datetime.now().date(),
                    city="SF", grad_year=2015,
                    time_period=10, searching=True)
        put = test_client.put('/api/user', data=data)
        self.check_valid_header_type(put.headers)
        data = json.loads(put.data)
        assert data['user']['nickname'] == "Alex"
        assert data['user']['netid'] == user.netid
        assert data['user']['city'] == "san francisco"

    def test_put_new_searcher_emails_matches(self, test_client, worker, outbox,
                                             sf_users, finished_sf_user):
        with test_client.session_transaction() as sess:
            sess['user_id'] = finished_sf_user.netid

        data = dict(nickname=finished_sf_user.nickname,
                    start_date=finished_sf_user.start_date,
                    city=finished_sf_user.city,
                    grad_year=finished_sf_user.grad_year,
                    time_period=finished_sf_user.time_period,
                    searching=True)
        put = test_client.put('/api/user', data=data)
        self.check_valid_header_type(put.headers)
        worker.work(burst=True)
        assert len(outbox) == 5
        assert "You have new potential roommate matches" in outbox[0].subject

    def test_put_new_searcher_does_not_pester_matches(self, test_client,
                                                      worker, outbox,
                                                      sf_user,
                                                      finished_sf_user):
        with test_client.session_transaction() as sess:
            sess['user_id'] = finished_sf_user.netid

        sf_user.last_emailed = datetime.now()

        data = dict(nickname=finished_sf_user.nickname,
                    start_date=finished_sf_user.start_date,
                    city=finished_sf_user.city,
                    grad_year=finished_sf_user.grad_year,
                    time_period=finished_sf_user.time_period,
                    searching=True)
        put = test_client.put('/api/user', data=data)
        self.check_valid_header_type(put.headers)
        worker.work(burst=True)
        assert len(outbox) == 0

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

    def test_matches_includes_finished_searchers(self, test_client,
                                                finished_sf_user, sf_user):
        with test_client.session_transaction() as sess:
            sess['user_id'] = sf_user.netid

        matches = test_client.get('/api/users/matches')
        self.check_valid_header_type(matches.headers)
        data = json.loads(matches.data)
        assert len(data['users']) == 1

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
