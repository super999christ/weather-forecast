import math

from rest_framework import serializers
from weather.models import Forecast


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class ForecastSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Forecast
        fields = ('description', 'temperature', 'pressure', 'humidity')

    def to_representation(self, instance):
        """Convert `username` to lowercase."""
        ret = super().to_representation(instance)

        # If temperature is requested change value from Kelvin to requested unit
        if 'temperature' in ret:
            temperature_units = self.context.get('temperature-units', 'K')
            ret['temperature'] = math.ceil(instance.convert_temperature(temperature_units))
            ret['temperature-units'] = temperature_units
        if 'pressure' in ret:
            ret['pressure-units'] = 'hPa'
        if 'humidity' in ret:
            ret['humidity'] = str(ret['humidity']) + '%'
            ret['humidity-units'] = 'percentage (%)'

        return ret
