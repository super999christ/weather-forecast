from datetime import datetime

from django.utils.encoding import force_text
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException

from weather.models import Forecast
from weather.serializers import ForecastSerializer


class WeatherException(APIException):
    """
    Custom APIException to return proper message in case of error.
    """
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'

    def __init__(self, detail, status_code):
        if status_code is not None:
            self.status_code = status_code
        if detail is not None:
            self.detail = force_text(detail)


class ForecastDetail(APIView):
    """
    Gets information about a forecast for a specific city given date and time.
    The allowed operation types are (summary, temperature, pressure, humidity).
    """

    @staticmethod
    def check_requested_time(requested_date, requested_hour):
        """
        Checks if the date and time requested correspond to the supported format.

        requested_date and requested_hour are enforced by the url to be integers
        so here only checks if they have a valid format.

        :param requested_date: the date present in the url of the request
        :param requested_hour: the time present in the url of the request
        :return: the requested_date and requested_hour as datetime objects
        """
        try:
            formatted_date = datetime.strptime(str(requested_date), '%Y%m%d')
            formatted_time = datetime.strptime(str(requested_hour), '%H%M')
        except (ValueError, TypeError):
            raise WeatherException('The requested date and/or time have an '
                                   'incorrect format. The correct format '
                                   'should be YYYYMMDD for date and HHMM for '
                                   'the time of the forecast',
                                   status.HTTP_400_BAD_REQUEST)

        return formatted_date, formatted_time

    @staticmethod
    def check_requested_operation(requested_operation):
        """
        Checks if the operation requested is one of the supported operations.

        Supported operations: summary, temperature, pressure, humidity

        :param requested_operation: the name of the forecast details operation
        """
        operation_name = requested_operation.lower()
        if operation_name not in ('summary', 'temperature', 'pressure',
                                  'humidity'):
            raise WeatherException('The requested operation is not supported. '
                                   'Please select on the supported operations '
                                   '(summary, temperature, pressure, humidity)',
                                   status.HTTP_400_BAD_REQUEST)
        return operation_name

    def get(self, request, operation_name, forecast_date, forecast_hour, format=None):

        requested_date, requested_time = self.check_requested_time(forecast_date,
                                                                  forecast_hour)
        requested_operation = self.check_requested_operation(operation_name)

        try:
            forecast = Forecast.objects.get(city__name='template',
                                            date=requested_date.date(),
                                            time=requested_time.time())
        except Forecast.DoesNotExist:
            raise WeatherException('Unfortunately there\'s no forecast data '
                                   'for {} {}'.format(
                                    requested_date.strftime('%Y-%m-%d'),
                                    requested_time.strftime('%H:%M')),
                                    status.HTTP_404_NOT_FOUND)

        serialize_fields = ('description', 'temperature', 'pressure',
                            'humidity')
        serialize_context = {'temperature-units': 'C'}

        # Since the names of the operations are equal to the model fields we
        # can just filter the serializer fields by the operation name
        if requested_operation in ('temperature', 'pressure', 'humidity'):
            serialize_fields = tuple(field for field in serialize_fields
                                     if field == operation_name)

        serializer = ForecastSerializer(forecast,
                                        fields=serialize_fields,
                                        context=serialize_context)
        return Response(serializer.data)
