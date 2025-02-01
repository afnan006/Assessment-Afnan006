import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))
from main import app

client = TestClient(app)

# Test Authorization for HubSpot
def test_authorize_hubspot_integration():
    response = client.post(
        "/integrations/hubspot/authorize",
        data={"user_id": "test_user", "org_id": "test_org"}
    )
    assert response.status_code == 200
    assert "authorization_url" in response.json()

# Test OAuth2 Callback for HubSpot
def test_oauth2callback_hubspot_integration():
    # Simulate a request from HubSpot OAuth2 callback
    response = client.get("/integrations/hubspot/oauth2callback?code=test_code")
    assert response.status_code == 200
    assert "access_token" in response.json()

# Test Get HubSpot Credentials
def test_get_hubspot_credentials_integration():
    response = client.post(
        "/integrations/hubspot/credentials",
        data={"user_id": "test_user", "org_id": "test_org"}
    )
    assert response.status_code == 200
    assert "credentials" in response.json()

# Test Loading HubSpot Items
def test_get_hubspot_items_integration():
    response = client.post(
        "/integrations/hubspot/get_hubspot_items",
        data={"credentials": "valid_credentials"}
    )
    assert response.status_code == 200
    assert "items" in response.json()
