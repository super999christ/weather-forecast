from behave import given, when, then
from django.core.management import call_command

from weather.models import City, Forecast


@when(u'I import the data from file {file_path}')
def import_weather_data_from_file(context, file_path):
    call_command('import_data', file_path)


@then(u'I should only have City object with name {city_name}')
def should_have_only_city_object(context, city_name):
    assert 1 == City.objects.count()
    assert City.objects.get(name=city_name) is not None


@then(u'I should have forecast objects for city {city_name}')
def should_have_only_forecast_objects(context, city_name):
    assert Forecast.objects.filter(city__name='template').count() > 0

    # get just the first one
    first_forecast = Forecast.objects.filter(city__name='template').order_by('-date')[0]
    assert first_forecast.date is not None
    assert first_forecast.time is not None
    assert first_forecast.temperature is not None
    assert first_forecast.pressure is not None
    assert first_forecast.humidity is not None
    assert first_forecast.description is not None
