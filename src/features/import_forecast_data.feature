Feature: Import Forecast Data
    In order to have forecast data to serve on the api
    As the Maintainer
    I want to import data and save database items

    Scenario: Imported city from data

      When I import the data from file ../config/template-forecast.json
      Then I should only have City object with name template

    Scenario: Imported forecasts for city

      When I import the data from file ../config/template-forecast.json
      Then I should have forecast objects for city template