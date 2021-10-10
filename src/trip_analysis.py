import pandas as pd
import datetime as dt
import numpy as np
from s2cell import lat_lon_to_cell_id


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

    def get_average_fare_heatmap(self, date: str, s2_level: int = 16):
        date = dt.datetime.strptime(date, "%Y-%m-%d").date()
        self.df["trip_start_date"] = self.df["trip_start_timestamp"].dt.date
        df = self.df[["pickup_latitude", "pickup_longitude"]].dropna()
        s2ids = df.apply(
            lambda row: lat_lon_to_cell_id(
                row.pickup_latitude, row.pickup_longitude, s2_level
            ),
            axis=1,
        )
        s2id_df = pd.DataFrame(s2ids, columns=["s2id"], index=s2ids.index).astype(str)
        df = pd.merge(self.df, s2id_df, left_index=True, right_index=True, how="left")
        in_date_range = df["trip_start_date"] == date
        df = df[["trip_start_date", "s2id", "fare"]]
        df = df[in_date_range].dropna()
        df = df.groupby("s2id").mean().reset_index()
        df["fare"] = round(df["fare"], 2)
        return df.to_dict("records")
