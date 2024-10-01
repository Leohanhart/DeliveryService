from fastapi.testclient import TestClient

from DeliveryServer.server.server import app

client = TestClient(app)


def test_fallback_route():
    response = client.get("/")
    assert response.status_code == 404
    assert response.json() == {
        "detail": f"This endpoint does not exist: {response.url}"
    }
