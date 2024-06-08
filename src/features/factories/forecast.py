import datetime

import factory
from weather.models import Forecast


class ForecastFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Forecast
        django_get_or_create = ('city', 'date', 'time', 'temperature',
                                'pressure', 'humidity', 'description')

    date = datetime.datetime(2018, 7, 28, 18, 00, 00).date()
    time = datetime.datetime(2018, 7, 28, 18, 00, 00).time()
    temperature = 294.15
    pressure = 1013.42
    humidity = 49
    description = 'light rain'
