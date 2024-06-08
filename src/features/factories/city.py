import datetime

import factory

from .forecast import ForecastFactory
from weather.models import City


class CityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = City
        django_get_or_create = ('name', 'country_code')

    # Defaults (can be overrided)
    name = 'template'
    country_code = 'gb'

    forecast_morning = factory.RelatedFactory(ForecastFactory, 'city',
                                              date=datetime.datetime(2018, 7, 29, 9, 00, 00).date(),
                                              time=datetime.datetime(2018, 7, 29, 9, 00, 00).time(),
                                              temperature=254.15,
                                              pressure=1003.42,
                                              humidity=70,
                                              description='cloudy')

    forecast_afternoon = factory.RelatedFactory(ForecastFactory, 'city',
                                                date=datetime.datetime(2018, 7, 29, 18, 00, 00).date(),
                                                time=datetime.datetime(2018, 7, 29, 18, 00, 00).time(),
                                                temperature=304.15,
                                                pressure=1023.42,
                                                humidity=23,
                                                description='sunny')

    forecast_night = factory.RelatedFactory(ForecastFactory, 'city',
                                            date=datetime.datetime(2018, 7, 29, 21, 00, 00).date(),
                                            time=datetime.datetime(2018, 7, 29, 21, 00, 00).time(),
                                            temperature=294.15,
                                            pressure=1013.42,
                                            humidity=49,
                                            description='light rain')
