import uvicorn
from fastapi import FastAPI, Query
from .trip_analysis import TaxiTripAnalyser

app = FastAPI()

data_source_path = "./data/chicago_taxi_trips_2020_processed.csv"
trip_analyser = TaxiTripAnalyser.load_from_processed_csv(data_source_path)

# enforcing date query format in HTTP handlers
date_query = Query(..., regex=r"[\d]{4}-[\d]{2}-[\d]{2}")


@app.get("/total_trips")
def total_trips(start: str = date_query, end: str = date_query):
    return {"data": trip_analyser.get_total_trips(start, end)}


@app.get("/average_fare_heatmap")
def average_fare_heatmap(date: str = date_query):
    return {"data": trip_analyser.get_average_fare_heatmap(date)}


@app.get("/average_speed_24hrs")
def average_speed_24hrs(date: str = date_query):
    return {"data": trip_analyser.get_average_speed_24hrs(date)}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
