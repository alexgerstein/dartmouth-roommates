from tests.factories import *

import string

from lodjers.models import User


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User

    netid = factory.fuzzy.FuzzyText(length=7, chars=string.hexdigits)
    full_name = factory.Sequence(lambda n: 'User %d' % n)

    city = factory.Sequence(lambda n: 'city %d' % n)
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
