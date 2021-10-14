# Chicago Taxi Trip Analysis

Author: Nithin Tom | [LinkedIn](https://www.linkedin.com/in/nithin-tom/)

Here, the goal is to build web APIs that provide basic analytics over the Chicago Taxi Trips dataset for the year 2020.

## Table of contents

1.  [Introduction](#introduction)

1.  [Usage](#usage)

1.  [Design](#design)

## Introduction

The web services are built using [FastAPI](https://fastapi.tiangolo.com/). The code is in python 3 and is dockerised. Three APIs are exposed:

- Total Trips per Day - Returns the total number of trips in the date range provided.
  `/total_trips?start=2020-01-01&end=2020-01-31`

- Average speed of trips (km/h) that ended in the past 24 hours from the provided date.
  `/average_speed_24hrs?date=2020-01-05`

- Fare Heatmap - The average fare per pick up location S2 ID at level 16 for the given date, based on the pickup time of the trip.
  `/average_fare_heatmap?date=2020-01-05`

## Usage

1.  To download the dataset, build the docker image and run the test suite:
    run `bin/setup`

2.  To run the web service:
    run `bin/run <OPTIONAL PORT>`

## Design

This project consist of the follwing main components.

1.  `src/trip_analysis.py`
    Contains the core logic for the analysis and it encapsulates all operations that have to do with working with the dataset including preprocessing and analytics logic.
    Two class methods are exposed to initialise the dataset as a pandas dataframe, from both the unprocessed file and the preprocessed file. During prepocessing, the columns required for supporting the APIs we expose are created upfront and all columns that are not needed are removed. The preprocessed file is then stored as a CSV since loading a CSV file into memory is quicker than loading a parquet file.
    For supporting the required operations, rows with any missing values among the required columns were dropped in the calculations.

2.  `src/prepare_data.py`
    Responsible for downloading the raw dataset, initiating the preprocessing step and storing the preprocessed data to disk for further use. This preprocessing will take a few mins because S2 ID calculation is done rowwise using the s2cell package due to lack of a better alternative.

3.  `src/services.py`
    Uses FastAPI to serve three APIs. Swagger documentation is provided by FastAPI out of the box and can be accessed through `http://<HOST>:<PORT>/docs`.

4.  `src/utils.py`
    Contains some utility functions that are reused multiple times elsewhere.

5.  `bin/setup`
    Builds a docker image using the included Dockerfile and requirements.txt file containing required pip packages. This also runs the test suite and prints the coverage report.

6.  `bin/run`
    Runs the docker container and start the API service. It runs on localhost:8080 by default, but a port number can be passed dynamically to make it run on a specific one on the client machine even though it runs on port 8080 inside the container.

7.  `config.json`
    Contains the dataset URL and local paths to store downloaded and preprocessed data.
