import pytest
from src.trip_analysis import TaxiTripAnalyser


@pytest.fixture(autouse=True)
def analyser():
    data_source_path = "./data/chicago_taxi_trips_2020_processed.csv"
    return TaxiTripAnalyser.load_from_processed_csv(data_source_path)


def test_get_total_trips(analyser):
    total_trips_dict = analyser.get_total_trips(
        start_date="2020-01-01", end_date="2020-01-03"
    )
    assert total_trips_dict[0] == {"date": "2020-01-01", "total_trips": 20798}
    assert total_trips_dict[1] == {"date": "2020-01-02", "total_trips": 26302}
    assert total_trips_dict[2] == {"date": "2020-01-03", "total_trips": 30795}


def test_get_average_speed_24hrs(analyser):
    average_speed_list = analyser.get_average_speed_24hrs(date="2020-01-02")
    assert average_speed_list[0]["average_speed"] == 23.31


def test_get_average_fare_heatmap(analyser):
    heatmap_list = analyser.get_average_fare_heatmap(date="2020-01-01")
    heatmap_dict = {}
    for heatmap in heatmap_list:
        heatmap_dict[str(heatmap["s2id"])] = heatmap["fare"]
    assert heatmap_dict["9803813108492271616"] == 43.79
    assert heatmap_dict["9803814005603565568"] == 10.72
