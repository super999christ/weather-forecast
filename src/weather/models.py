from django.db import models


class City(models.Model):
    """
    Represents the different cities with weather forecast
    """
    name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=10)

    def __str__(self):
        return '{}, {}'.format(self.name, self.country_code)


class Forecast(models.Model):
    """
    Represents the weather forecast associated to the cities
    """
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    # temperatures saved with Unit as Kelvin
    temperature = models.FloatField()
    max_temperature = models.FloatField(null=True)
    min_temperature = models.FloatField(null=True)
    # pressures saved with unit as Atmospheric pressure (hPa)
    pressure = models.FloatField()
    pressure_at_sea = models.FloatField(null=True)
    pressure_at_ground = models.FloatField(null=True)
    # humidity and cloudiness as percentage
    humidity = models.FloatField()
    cloudiness = models.FloatField(null=True)
    description = models.CharField(max_length=250)
    # wind speed as meter/sec
    wind_speed = models.FloatField(null=True)
    wind_degrees = models.FloatField(null=True)

    def __str__(self):
        return 'Forecast for {} on {} at {}'.format(self.city.name,
                                                    str(self.date),
                                                    str(self.time))

    def convert_temperature(self, convert_unit='K'):
        """
        Converts temperature field from Kelvin to requested unit.
        Kelvin (K), Celsius (C), Fahrenheit (F).
        :param convert_unit: K, C, F
        :return: converted temperature
        """
        if convert_unit == 'C':
            return self.temperature - 273.15
        elif convert_unit == 'F':
            return (self.temperature - 9 / 5) - 459.67
        else:
            return self.temperature
