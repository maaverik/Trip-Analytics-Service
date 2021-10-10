from fastapi.testclient import TestClient
from src.services import app

client = TestClient(app)


def test_total_trips():
    response = client.get("/total_trips?start=2020-01-01&end=2020-01-05")
    assert response.status_code == 200

    response = client.get("/total_trips?start=2020-01-01&end=2020-01-xx")
    assert response.status_code == 422

    response = client.get("/total_trips?start=2020-01-01&end=2020-0100")
    assert response.status_code == 422

    response = client.get("/total_trips?start=2020-01-01&end=2020-01")
    assert response.status_code == 422


def test_average_fare_heatmap():
    response = client.get("/average_fare_heatmap?date=2020-01-01")
    assert response.status_code == 200

    response = client.get("/average_fare_heatmap?date=2020-01-xx")
    assert response.status_code == 422

    response = client.get("/average_fare_heatmap?date=2020-0100")
    assert response.status_code == 422

    response = client.get("/average_fare_heatmap?date=2020-01")
    assert response.status_code == 422


def test_average_speed_24hrs():
    response = client.get("/average_speed_24hrs?date=2020-01-01")
    assert response.status_code == 200

    response = client.get("/average_speed_24hrs?date=2020-01-xx")
    assert response.status_code == 422

    response = client.get("/average_speed_24hrs?date=2020-0100")
    assert response.status_code == 422

    response = client.get("/average_speed_24hrs?date=2020-01")
    assert response.status_code == 422
