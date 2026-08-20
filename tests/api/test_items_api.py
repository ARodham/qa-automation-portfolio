import pytest

from utils.api_client import ApiClient
from utils.config import base_url


@pytest.fixture
def api() -> ApiClient:
    return ApiClient(base_url())


@pytest.mark.smoke
def test_health_endpoint_reports_ok(api: ApiClient):
    response = api.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.smoke
def test_inventory_list_has_expected_contract(api: ApiClient):
    response = api.get("/api/items")

    assert response.status_code == 200
    body = response.json()

    assert body["count"] == len(body["items"])
    assert body["count"] > 0

    required_fields = {"id", "name", "category", "in_stock"}
    for item in body["items"]:
        assert required_fields.issubset(item)


@pytest.mark.regression
def test_known_inventory_item_can_be_retrieved(api: ApiClient):
    response = api.get("/api/items/1")

    assert response.status_code == 200
    assert response.json()["name"] == "Wireless Headset"


@pytest.mark.regression
def test_unknown_inventory_item_returns_404(api: ApiClient):
    response = api.get("/api/items/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"


@pytest.mark.regression
def test_create_item_returns_created_resource(api: ApiClient):
    payload = {"name": "Webcam", "category": "Video"}

    response = api.post("/api/items", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["name"] == payload["name"]
    assert body["category"] == payload["category"]
    assert body["in_stock"] is True


@pytest.mark.regression
def test_invalid_item_payload_is_rejected(api: ApiClient):
    response = api.post(
        "/api/items",
        json={"name": "", "category": "X"},
    )

    assert response.status_code == 422
