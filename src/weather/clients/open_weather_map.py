import datetime


class OpenWeatherException(Exception):
    def __init__(self, message, errors):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

        # Now for your custom code...
        self.errors = errors


class OpenWeatherMap(object):
    """
    Represents a client to communicate and process data from OpenWeatherMap
    https://openweathermap.org
    """
    @classmethod
    def process_city_forecasts(cls, city_forecast):
        """
        Processes forecast data specific to a city from openWeatherMap.
        The format of the data is explained at: openweathermap.org/forecast5

        :param city_forecast: Forecasts for a specific city in json format
        :return: city info and associated forecasts
        """
        if ('city' not in city_forecast or
                ('name' not in city_forecast['city'] and
                 'country' not in city_forecast['city'])):
            raise OpenWeatherException('Json data doesnt contain required city'
                                       ' information')

        city = city_forecast['city']
        city_name = city['name']
        city_country = city['country']
        forecasts = city_forecast['list']

        processed_forecasts = []
        for forecast in forecasts:
            try:
                forecast_datetime = datetime.datetime.fromtimestamp(int(forecast['dt']))
            except ValueError:
                raise OpenWeatherException('Invalid timestamp from json data')

            try:
                main_forecast_info = forecast['main']
                forecast_description = forecast['weather'][0]   # Only the first description is necessary.
                cloud_forecast = forecast['clouds']
                wind_forecast = forecast['wind']
            except KeyError as error:
                raise OpenWeatherException('Json data does not contain required'
                                           ' forecast info: %s', error)

            processed_forecast = {
                'date': forecast_datetime.date(),
                'time': forecast_datetime.time(),
                'temperature': main_forecast_info.get('temp'),
                'max_temperature': main_forecast_info.get('temp_max'),
                'min_temperature': main_forecast_info.get('temp_min'),
                'pressure': main_forecast_info.get('pressure'),
                'pressure_at_sea': main_forecast_info.get('sea_level'),
                'pressure_at_ground': main_forecast_info.get('rnd_level'),
                'humidity': main_forecast_info.get('humidity'),
                'cloudiness': cloud_forecast.get('all'),
                'description': forecast_description.get('description'),
                'wind_speed': wind_forecast.get('speed'),
                'wind_degrees': wind_forecast.get('deg'),
            }
            processed_forecasts.append(processed_forecast)

        city_info = {
            'name': city_name.lower(),
            'country_code': city_country.lower(),
            'forecasts': processed_forecasts,
        }

        return city_info
