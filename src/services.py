import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.trip_analysis import TaxiTripAnalyser
from src.utils import get_config, is_valid_iso_date

app = FastAPI()

config = get_config()
data_source_path = config["processed_data_path"]
trip_analyser = TaxiTripAnalyser.load_from_processed_csv(data_source_path)


class InvalidDateException(Exception):
    def __init__(self, date: str):
        self.date = date


@app.exception_handler(InvalidDateException)
async def invalid_date_exception_handler(request: Request, exc: InvalidDateException):
    return JSONResponse(
        status_code=422,
        content={
            "error": f"The value {exc.date} is not a valid ISO date 8601 formatted date"
        },
    )


@app.get("/total_trips")
def total_trips(start: str, end: str):
    if not is_valid_iso_date(start):
        raise InvalidDateException(start)
    if not is_valid_iso_date(end):
        raise InvalidDateException(end)
    return {"data": trip_analyser.get_total_trips(start, end)}


@app.get("/average_fare_heatmap")
def average_fare_heatmap(date: str):
    if not is_valid_iso_date(date):
        raise InvalidDateException(date)
    return {"data": trip_analyser.get_average_fare_heatmap(date)}


@app.get("/average_speed_24hrs")
def average_speed_24hrs(date: str):
    if not is_valid_iso_date(date):
        raise InvalidDateException(date)
    return {"data": trip_analyser.get_average_speed_24hrs(date)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
