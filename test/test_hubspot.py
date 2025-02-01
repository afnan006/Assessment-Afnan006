# import sys
# import os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))
# from main import app

# client = TestClient(app)

# # Test Authorization for HubSpot
# def test_authorize_hubspot_integration():
#     response = client.post(
#         "/integrations/hubspot/authorize",
#         data={"user_id": "test_user", "org_id": "test_org"}
#     )
#     assert response.status_code == 200
#     assert "authorization_url" in response.json()

# # Test OAuth2 Callback for HubSpot
# def test_oauth2callback_hubspot_integration():
#     # Simulate a request from HubSpot OAuth2 callback
#     response = client.get("/integrations/hubspot/oauth2callback?code=test_code")
#     assert response.status_code == 200
#     assert "access_token" in response.json()

# # Test Get HubSpot Credentials
# def test_get_hubspot_credentials_integration():
#     response = client.post(
#         "/integrations/hubspot/credentials",
#         data={"user_id": "test_user", "org_id": "test_org"}
#     )
#     assert response.status_code == 200
#     assert "credentials" in response.json()

# # Test Loading HubSpot Items
# def test_get_hubspot_items_integration():
#     response = client.post(
#         "/integrations/hubspot/get_hubspot_items",
#         data={"credentials": "valid_credentials"}
#     )
#     assert response.status_code == 200
#     assert "items" in response.json()
import sys
import os
import pytest
import json
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))
from main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_redis():
    with patch("integrations.hubspot.get_value_redis") as mock_get:
        mock_get.return_value = None
        yield

def test_authorize_hubspot_integration():
    with patch("integrations.hubspot.add_key_value_redis") as mock_redis:
        mock_redis.return_value = AsyncMock()
        response = client.post(
            "/integrations/hubspot/authorize",
            data={"user_id": "test_user", "org_id": "test_org"}
        )
        assert response.status_code == 200
        assert "auth_url" in response.json()

def test_get_hubspot_items_integration():
    with patch("integrations.hubspot.get_value_redis") as mock_get:
        mock_get.return_value = json.dumps({
            "access_token": "test_token",
            "refresh_token": "test_refresh",
            "expires_in": 3600
        })
        
        with patch("httpx.AsyncClient.get") as mock_api:
            mock_api.return_value = AsyncMock(
                status_code=200,
                json=lambda: {
                    "results": [{
                        "id": "test_id",
                        "properties": {"firstname": "Test"},
                        "createdAt": "2024-01-01T00:00:00Z",
                        "updatedAt": "2024-01-01T00:00:00Z"
                    }]
                }
            )
            response = client.post(
                "/integrations/hubspot/load",
                data={"user_id": "test_user", "org_id": "test_org"}
            )
            assert response.status_code == 200
            assert "items" in response.json()