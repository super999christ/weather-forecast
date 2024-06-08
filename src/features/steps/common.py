import json

from behave import when, given, then

from factories.city import CityFactory


@given('the system contains forecast data')
def create_data(context):
    u = CityFactory()
    u.save()    # Don't omit to call save() to insert object in database


@when(u'I visit "{url}"')
def visit(context, url):
    context.response = context.test.client.get(url)


@then(u'it should return response an OK status code')
def it_should_be_the_correct_status_code(context):
    assert context.response.status_code == 200


@then(u'it should return an error status code {status_code}')
def it_should_be_the_correct_status_code(context, status_code):
    assert context.response.status_code == int(status_code)


@then(u'it should return an informative error message {error_response}')
def it_should_be_an_informative_error(context, error_response):
    api_response = json.loads(context.response.content)
    test_response = json.loads(error_response)
    assert api_response == test_response
