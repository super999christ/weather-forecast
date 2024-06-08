import json
import sys

from behave import then


@then(u'it should contain the forecast details content {details_response}')
def it_should_be_the_forecast_details(context, details_response):
    api_response = json.loads(context.response.content)
    test_response = json.loads(details_response)

    assert api_response == test_response
