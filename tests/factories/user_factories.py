from tests.factories import *

import string

from dartmates.models import User


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User

    netid = factory.fuzzy.FuzzyText(length=7, chars=string.hexdigits)
    full_name = factory.Sequence(lambda n: 'User %d' % n)

    city = factory.Sequence(lambda n: 'City %d' % n)
    number_of_roommates = factory.fuzzy.FuzzyInteger(5)
    start_date = factory.fuzzy.FuzzyDate(datetime.date(2015, 6, 10),
                                         datetime.date(2018, 6, 10))
    time_period = factory.fuzzy.FuzzyInteger(24)
    grad_year = factory.fuzzy.FuzzyInteger(2015, 2020)
    searching = True

    email_updates = True
