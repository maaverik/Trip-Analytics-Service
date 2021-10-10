import uvicorn
from fastapi import FastAPI, Query


app = FastAPI()

# enforcing date query format in HTTP handlers
date_query = Query(..., regex=r"[\d]{4}-[\d]{2}-[\d]{2}")


@app.get("/total_trips")
def total_trips(start: str = date_query, end: str = date_query):
    return {"start_date": start, "end_date": end}


@app.get("/average_fare_heatmap")
def average_fare_heatmap(date: str = date_query):
    return {"date": date}


@app.get("/average_speed_24hrs")
def average_speed_24hrs(date: str = date_query):
    return {"date": date}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
