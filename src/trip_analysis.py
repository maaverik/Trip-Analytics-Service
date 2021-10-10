import pandas as pd
import datetime as dt
import numpy as np


class TaxiTripAnalyser:
    def __init__(self, data_source_path):
        self.df = pd.read_parquet(data_source_path).reset_index(drop=True)

    def pre_process_df(self):
        raise NotImplementedError()

    def get_total_trips(self, start_date: str, end_date: str):
        start_date = dt.datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = dt.datetime.strptime(end_date, "%Y-%m-%d").date()

        self.df["trip_start_date"] = self.df["trip_start_timestamp"].dt.date

        in_date_range = (self.df["trip_start_date"] >= start_date) & (
            self.df["trip_start_date"] <= end_date
        )

        df = self.df[in_date_range]
        df["trip_start_date"] = df["trip_start_date"].astype(str)
        trips = df.groupby("trip_start_date").count()
        trips = trips.reset_index()
        trips = trips.rename(
            columns={"trip_start_date": "date", "unique_key": "total_trips"}
        )
        trips = trips[["date", "total_trips"]]
        return trips.to_dict("records")
