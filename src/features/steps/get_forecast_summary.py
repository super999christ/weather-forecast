import json

from behave import then


@then(u'it should contain the forecast summary content {summary_response}')
def it_should_be_the_forecast_summary(context, summary_response):
    api_response = json.loads(context.response.content)
    test_response = json.loads(summary_response)

    assert api_response.get('description') == test_response.get('description')
    assert api_response.get('temperature') == test_response.get('temperature')
    assert api_response.get('pressure') == test_response.get('pressure')
    assert api_response.get('humidity') == test_response.get('humidity')
    assert api_response.get('temperature-units') == test_response.get('temperature-units')
    assert api_response.get('pressure-units') == test_response.get('pressure-units')
    assert api_response.get('humidity-units') == test_response.get('humidity-units')
