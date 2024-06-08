Feature: Get Forecast Details
    As a user of the system I want to get the forecast details for the
    city requested and for the date and time requested.

    Scenario Outline: Access forecast details

        Given the system contains forecast data
        When I visit "<url>"
        Then it should return response an OK status code
        And it should contain the forecast details content <details_response>

    Examples: Morning forecast
       | url        | details_response |
       | /weather/temperature/template/20180729/0900/ | {"temperature": -18, "temperature-units": "C" } |
       | /weather/pressure/template/20180729/0900/ | {"pressure": 1003.42, "pressure-units": "hPa"} |
       | /weather/humidity/template/20180729/0900/ | {"humidity": "70.0%", "humidity-units": "percentage (%)"} |

    Examples: Afternoon and Night forecasts
       | url        | details_response |
       | /weather/temperature/template/20180729/1800/  | {"temperature": 31, "temperature-units": "C"} |
       | /weather/pressure/template/20180729/1800/  | {"pressure": 1023.42, "pressure-units": "hPa"} |
       | /weather/humidity/template/20180729/1800/  | {"humidity": "23.0%", "humidity-units": "percentage (%)"} |
       | /weather/temperature/template/20180729/2100/  | {"temperature": 21, "temperature-units": "C"} |
       | /weather/pressure/template/20180729/2100/  | {"pressure": 1013.42, "pressure-units": "hPa"} |
       | /weather/humidity/template/20180729/2100/  | {"humidity": "49.0%", "humidity-units": "percentage (%)"} |


    Scenario Outline: Get informative error messages

        Given the system contains forecast data
        When I visit "<url>"
        Then it should return an error status code <status_code>
        And it should return an informative error message <error_response>

    Examples: Not supported operation type
       | url        | status_code | error_response |
       | /weather/not_existant/template/20180729/0900/ | 400 | {"detail": "The requested operation is not supported. Please select on the supported operations (summary, temperature, pressure, humidity)", "status": "error", "status_code": 400} |

    Examples: Wrong format on date parameter
       | url        | status_code | error_response |
       | /weather/temperature/template/2029/0900/ | 400 | {"detail": "The requested date and/or time have an incorrect format. The correct format should be YYYYMMDD for date and HHMM for the time of the forecast", "status": "error", "status_code": 400} |
       | /weather/pressure/template/2029/0900/ | 400 | {"detail": "The requested date and/or time have an incorrect format. The correct format should be YYYYMMDD for date and HHMM for the time of the forecast", "status": "error", "status_code": 400} |
       | /weather/humidity/template/2029/0900/ | 400 | {"detail": "The requested date and/or time have an incorrect format. The correct format should be YYYYMMDD for date and HHMM for the time of the forecast", "status": "error", "status_code": 400} |

    Examples: Wrong format on time parameter
       | url        | status_code | error_response |
       | /weather/temperature/template/20180729/9/ | 400 | {"detail": "The requested date and/or time have an incorrect format. The correct format should be YYYYMMDD for date and HHMM for the time of the forecast", "status": "error", "status_code": 400} |
       | /weather/pressure/template/2029/0900/ | 400 | {"detail": "The requested date and/or time have an incorrect format. The correct format should be YYYYMMDD for date and HHMM for the time of the forecast", "status": "error", "status_code": 400} |
       | /weather/humidity/template/2029/0900/ | 400 | {"detail": "The requested date and/or time have an incorrect format. The correct format should be YYYYMMDD for date and HHMM for the time of the forecast", "status": "error", "status_code": 400} |


    Scenario Outline: The system does not have information about forecast

        Given the system contains forecast data
        When I visit "<url>"
        Then it should return an error status code <status_code>
        And it should return an informative error message <error_response>
        
    Examples: No forecast for the requested date and time
       | url        | status_code | error_response |
       | /weather/temperature/template/20170729/0900/ | 404 | {"detail": "Unfortunately there's no forecast data for 2017-07-29 09:00", "status": "error", "status_code": 404} |
       | /weather/pressure/template/20180729/1000/ | 404 | {"detail": "Unfortunately there's no forecast data for 2018-07-29 10:00", "status": "error", "status_code": 404 } |
       | /weather/humidity/template/20180729/1000/ | 404 | {"detail": "Unfortunately there's no forecast data for 2018-07-29 10:00", "status": "error", "status_code": 404 } |


    Scenario: Access forecast details after getting the summary

      Given the system contains forecast data
      When I visit "/weather/summary/template/20180729/0900/"
      Then it should return response an OK status code
      And it should contain the forecast summary content {"description": "cloudy", "temperature": -18, "pressure": 1003.42, "humidity": "70.0%", "temperature-units": "C", "pressure-units": "hPa", "humidity-units": "percentage (%)"}
      When I visit "/weather/temperature/template/20180729/0900/"
      Then it should return response an OK status code
      And it should contain the forecast details content {"temperature": -18, "temperature-units": "C" }
