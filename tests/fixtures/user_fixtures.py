import pytest
from tests.factories import user_factories
import datetime


@pytest.fixture()
def user(request):
    return user_factories.UserFactory()


@pytest.fixture()
def sf_user(request):
    return user_factories.SanFranciscoUserFactory()


@pytest.fixture()
def sf_users(request):
    return user_factories.SanFranciscoUserFactory.create_batch(5)


@pytest.fixture()
def female_sf_user(request):
    return user_factories.SanFranciscoUserFactory(gender="F")


@pytest.fixture()
def old_sf_user(request):
    return user_factories. \
           SanFranciscoUserFactory(start_date=datetime.date(2000, 1, 1))


@pytest.fixture()
def finished_sf_user(request):
    return user_factories.SanFranciscoUserFactory(searching=False)


@pytest.fixture()
def ny_user(request):
    return user_factories.SanFranciscoUserFactory(city="new york")
