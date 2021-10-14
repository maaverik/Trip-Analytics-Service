import uvicorn
from fastapi import FastAPI, Query
from src.trip_analysis import TaxiTripAnalyser
from src.utils import get_config

app = FastAPI()

config = get_config()
data_source_path = config["processed_data_path"]
trip_analyser = TaxiTripAnalyser.load_from_processed_csv(data_source_path)

# enforcing date query format in HTTP handlers
date_query_format = Query(..., regex=r"[\d]{4}-[\d]{2}-[\d]{2}$")


@app.get("/total_trips")
def total_trips(start: str = date_query_format, end: str = date_query_format):
    return {"data": trip_analyser.get_total_trips(start, end)}


@app.get("/average_fare_heatmap")
def average_fare_heatmap(date: str = date_query_format):
    return {"data": trip_analyser.get_average_fare_heatmap(date)}


@app.get("/average_speed_24hrs")
def average_speed_24hrs(date: str = date_query_format):
    return {"data": trip_analyser.get_average_speed_24hrs(date)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
