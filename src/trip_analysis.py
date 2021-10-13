import pandas as pd
import datetime as dt
import numpy as np
import math
import logging
import sys
from s2cell import lat_lon_to_cell_id

pd.options.mode.chained_assignment = None  # suppress SettingWithCopy warning
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()


class TaxiTripAnalyser:
    def __init__(self, df):
        self.df = df

    @classmethod
    def load_from_unprocessed_parquet(cls, data_source_path):
        logger.info("Loading unprocessed parquet file...")
        df = pd.read_parquet(data_source_path).reset_index(drop=True)
        df = cls.pre_process_df(df)
        processed_df_path = data_source_path.replace(".parquet", "_processed.csv")
        logger.info(f"Saving processed dataframe at {processed_df_path}...")
        df.to_csv(processed_df_path, index=False)
        return cls(df)

    @classmethod
    def load_from_processed_csv(cls, data_source_path):
        logger.info(f"Loading processed dataframe from {data_source_path}...")
        df = pd.read_csv(data_source_path)
        df = df.replace([""], np.nan)
        return cls(df)

    @classmethod
    def pre_process_df(cls, df, s2_level: int = 16):
        logger.info(
            "Preprocessing the input dataframe, this will take a few minutes..."
        )
        required_columns = [
            "unique_key",
            "trip_start_timestamp",
            "trip_end_timestamp",
            "trip_miles",
            "trip_seconds",
            "pickup_latitude",
            "pickup_longitude",
            "fare",
        ]
        df = df[required_columns]  # to speed up subsequent operations

        df = cls.add_date(df)
        df = cls.add_speed(df)
        df = cls.add_s2id(df, s2_level)

        required_columns = [
            "unique_key",
            "trip_start_date",
            "trip_end_date",
            "speed",
            "s2id",
            "fare",
        ]
        df = df[required_columns]  # only store required columns
        logger.debug("Preprocessing complete")
        return df

    @staticmethod
    def add_date(df):
        logger.info("Adding date columns...")
        df["trip_start_date"] = df["trip_start_timestamp"].dt.date.astype(str)
        df["trip_end_date"] = df["trip_end_timestamp"].dt.date.astype(str)
        return df

    @staticmethod
    def add_speed(df):
        logger.info("Adding speed column...")
        unit_conversion_factor = 1.609 * 3600
        df["speed"] = (df["trip_miles"] / df["trip_seconds"]) * unit_conversion_factor
        df["speed"] = df["speed"].replace([np.inf], np.nan)
        return df

    @staticmethod
    def add_s2id(df, s2_level: int = 16):
        logger.info("Adding s2id column...")
        df_temp = df[["pickup_latitude", "pickup_longitude"]].dropna()
        s2ids = df_temp.apply(
            lambda row: lat_lon_to_cell_id(
                row.pickup_latitude, row.pickup_longitude, s2_level
            ),
            axis=1,
        )
        s2id_df = pd.DataFrame(s2ids, columns=["s2id"], index=s2ids.index).astype(str)
        df = pd.merge(df, s2id_df, left_index=True, right_index=True, how="left")
        return df

    def get_total_trips(self, start_date: str, end_date: str):
        df = self.df
        in_date_range = (df["trip_start_date"] >= start_date) & (
            df["trip_start_date"] <= end_date
        )
        df = df[in_date_range]
        trips = df.groupby("trip_start_date").count()
        trips = trips.reset_index()
        trips = trips.rename(
            columns={"trip_start_date": "date", "unique_key": "total_trips"}
        )
        trips = trips[["date", "total_trips"]]
        return trips.to_dict("records")

    def get_average_speed_24hrs(self, date: str):
        df = self.df
        date = dt.datetime.strptime(date, "%Y-%m-%d").date()
        previous_date = str(date - dt.timedelta(days=1))
        in_date_range = df["trip_end_date"] == previous_date
        df = df[in_date_range]
        average_speed = df["speed"].dropna().mean()
        average_speed = round(average_speed, 2)
        if math.isnan(average_speed) or math.isinf(average_speed):
            average_speed = "NaN"
        return [{"average_speed": average_speed}]

    def get_average_fare_heatmap(self, date: str):
        df = self.df
        df = df[["trip_start_date", "s2id", "fare"]]
        in_date_range = df["trip_start_date"] == date
        df = df[in_date_range].dropna()
        df = df.groupby("s2id")["fare"].mean().reset_index()
        df["fare"] = round(df["fare"], 2)
        return df.to_dict("records")
