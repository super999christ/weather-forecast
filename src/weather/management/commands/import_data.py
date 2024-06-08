import json

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import MultipleObjectsReturned

from weather.clients.open_weather_map import OpenWeatherMap, OpenWeatherException
from weather.models import City, Forecast


class Command(BaseCommand):
    help = ('Imports weather forecast from OpenWeather. '
            'Argument is file path to json formatted file(s) representing a '
            'city forecast')

    def add_arguments(self, parser):
        parser.add_argument('file_path', nargs='+', type=str)

    def handle(self, *args, **options):
        for file_path in options['file_path']:
            with open(file_path, 'r') as weather_file:
                json_data = json.load(weather_file)
                try:
                    city_forecast = OpenWeatherMap.process_city_forecasts(json_data)
                except OpenWeatherException as import_error:
                    raise CommandError(import_error.message)

                # Pops the forecasts to make is easier to create new city
                forecasts = city_forecast.pop('forecasts')

                # Get or create City
                try:
                    city_record, created = City.objects.get_or_create(**city_forecast)
                except MultipleObjectsReturned:
                    # Gets only one city and warns the user
                    city_record = City.objects.filter(name=city_forecast.get('name'),
                                                      country_code=city_forecast.get('country_code'))[0]
                    self.stderr.write(self.style.WARNING('Multiple records '
                                                         'returned for %s'
                                                         % city_forecast.get('name')))

                # Update of create forecasts for the city
                for forecast in forecasts:
                    try:
                        obj = Forecast.objects.get(city=city_record,
                                                   date=forecast.get('date'),
                                                   time=forecast.get('time'))
                        for key, value in forecast.items():
                            setattr(obj, key, value)
                        obj.save()
                    except Forecast.DoesNotExist:
                        obj = Forecast(city=city_record, **forecast)
                        obj.save()

                self.stdout.write(self.style.SUCCESS('Successfully imported '
                                                     'data of "%s"' % file_path))
