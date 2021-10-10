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

    def get_average_speed_24hrs(self, date: str):
        unit_conversion_factor = 1.609 * 3600
        self.df["speed"] = (
            self.df["trip_miles"] / self.df["trip_seconds"]
        ) * unit_conversion_factor
        self.df["speed"] = self.df["speed"].replace([np.inf], np.nan)
        self.df["trip_end_date"] = self.df["trip_end_timestamp"].dt.date

        date = dt.datetime.strptime(date, "%Y-%m-%d").date()
        previous_date = date - dt.timedelta(days=1)
        in_date_range = self.df["trip_end_date"] == previous_date
        df = self.df[in_date_range]
        average_speed = df["speed"].dropna().mean()
        return round(average_speed, 2)
