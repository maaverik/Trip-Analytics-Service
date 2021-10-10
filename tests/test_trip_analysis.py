import pytest
from src.trip_analysis import TaxiTripAnalyser


@pytest.fixture(autouse=True)
def analyser():
    data_source_path = "./data/chicago_taxi_trips_2020.parquet"
    return TaxiTripAnalyser(data_source_path)


def test_get_total_trips(analyser):
    total_trips_dict = analyser.get_total_trips(
        start_date="2020-01-01", end_date="2020-01-03"
    )
    assert total_trips_dict[0] == {"date": "2020-01-01", "total_trips": 20798}
    assert total_trips_dict[1] == {"date": "2020-01-02", "total_trips": 26302}
    assert total_trips_dict[2] == {"date": "2020-01-03", "total_trips": 30795}