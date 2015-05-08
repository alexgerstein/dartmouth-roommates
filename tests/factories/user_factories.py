from tests.factories import *

from faker import Factory as FakerFactory

from lodjers.models import User

faker = FakerFactory.create()


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User

    netid = factory.LazyAttribute(lambda x: faker.bothify('?#####?'))
    full_name = factory.Sequence(lambda n: faker.name())
    gender = "M"

    city = factory.Sequence(lambda n: faker.city())
    start_date = factory.fuzzy.FuzzyDate(date(2015, 6, 10),
                                         date(2018, 6, 10))
    time_period = factory.fuzzy.FuzzyInteger(24)
    grad_year = factory.fuzzy.FuzzyInteger(2015, 2020)
    searching = True

    email_updates = True
    last_emailed = datetime.min


class SanFranciscoUserFactory(UserFactory):
    city = "san francisco"
    start_date = date(2015, 7, 3)
    time_period = 12
