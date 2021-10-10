import uvicorn
from fastapi import FastAPI, Query


app = FastAPI()


@app.get("/total_trips")
def total_trips(start: str, end: str):
    return {"start_date": start, "end_date": end}


@app.get("/average_fare_heatmap")
def average_fare_heatmap(date: str):
    return {"date": date}


@app.get("/average_speed_24hrs")
def average_speed_24hrs(date: str):
    return {"date": date}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
