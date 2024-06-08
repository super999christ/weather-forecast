# Weather Forecast 
Python APIs using Django Rest Framework to acquire the Weather Forecast (from OpenWeather)

## Usage:
`http://<domain>/weather/<operation>/template/<date>/<time>/`

You can select: 

- operation - Types of operations supported (summary, temperature, pressure, humidity)
- date - Day of the forecast with the format YYYYMMDD
- time - Time of the forecast with the format HHMM (currently the forecasts are separated between 3h e.g: 0900, 1200, 1500, 1800, 2100)

### Examples:

`http://localhost:8000/weather/summary/template/20180729/1800/
http://localhost:8000/weather/summary/template/20180727/0900/
http://localhost:8000/temperature/summary/template/20180729/1800/`

## Instructions for how to set up and get the service running:

1. `git clone https://github.com/super999christ/weather-forecast.git`

### With docker installed (without docker-compose installed):
2. `cd weather-forecast/`
3. `docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v "$PWD:$PWD" -w="$PWD" docker/compose:1.22.0 up`

The container is now running and it's possible to check the logs of the requests

4. Go to `http://localhost:8000/weather/summary/template/20180729/1800/`
5. `CTRL/CMD+C to stop the container`

#### In the case of not wanting to copy the compose command everytime is possible to create an alias
6. `echo alias docker-compose="'"'docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v "$PWD:$PWD" -w="$PWD" docker/compose:1.2.0'"'" >> ~/.bashrc`
7. `source ~/.bashrc`

##### The alias is necessary in case of wanting to run the test inside the container
8. `docker-compose start` runs the service on the background
9. `docker exec -ti dg01 bash` to enter the command line inside the container
10. To run the tests: `python manage.py behave`
11. `docker-compose stop` stops the service

### With docker installed (with docker-compose):
2. `pip install docker-compose`
3. `cd weather_forecast/`
4. For first time running the containers `run docker-compose up -d` and `docker-compose build` for the rebuilds

The container is now running

5. Go to `http://localhost:8000/weather/summary/template/20180729/1800/`
6. `docker exec -ti dg01 bash` to enter the command line inside the container
7. To run the tests: `python manage.py behave`
8. `docker-compose stop` stops the service

#### Other usefull docker commands to clean up after:
- docker rm $(docker ps -a -q)# Delete all containers
- docker rmi $(docker images -q) # Delete all images

### Without docker

*Note:* This steps should be executed inside a virtual environment

2. `cd weather_forecast/`
3. `pip install -r config/requirements.pip`
4. `cd src/`
5. `python manage.py makemigrations` 
6. `python manage.py makemigrations weather` 
7. `python manage.py migrate`
8. `python manage.py import_data ../config/template-forecast.json`
9. `python manage.py runserver`
10. Go to `http://localhost:8000/weather/summary/template/20180729/1800/`

*Note:* To run this locally you need to go to the /weatherforecst/setting.py file and change the `ALLOWED_HOSTS = ['web']` to `ALLOWED_HOSTS = ['*']` (don't do this in production)

7. To run the tests: `python manage.py behave`
