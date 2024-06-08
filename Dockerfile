# Dockerfile

# FROM directive instructing base image to build upon
FROM python:3.6

ENV PYTHONUNBUFFERED 1

# Create config directory
RUN mkdir /config

# Add requirements file to config directory
ADD /config/requirements.pip /config/

# Add json data for initial import to config directory
ADD /config/template-forecast.json /config/

# Install requirements
RUN pip install -r /config/requirements.pip

RUN mkdir /src;

# set project WORKDIR
WORKDIR /src
