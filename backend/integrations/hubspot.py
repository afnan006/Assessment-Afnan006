from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
import httpx
import json
import secrets
import base64
from dotenv import load_dotenv
import os
from datetime import datetime
from integrations.integration_item import IntegrationItem
from redis_client import add_key_value_redis, get_value_redis, delete_key_redis
import logging
import os

load_dotenv() 
logging.basicConfig(level=logging.DEBUG)
# Create a FastAPI router
router = APIRouter()

# HubSpot OAuth Credentials
CLIENT_ID = os.getenv("HUBSPOT_CLIENT_ID")
CLIENT_SECRET = os.getenv("HUBSPOT_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8000/integrations/hubspot/oauth2callback"

# Scopes required for HubSpot integration
SCOPES = (
    "crm.objects.contacts.read crm.objects.contacts.write "
    "crm.objects.companies.read crm.objects.deals.read "
    "tickets oauth automation crm.schemas.custom.read crm.objects.custom.read"
)

# Debugging: Print environment variables
print(f"CLIENT_ID: {CLIENT_ID}")
print(f"CLIENT_SECRET: {CLIENT_SECRET}")

@router.post("/authorize")
async def authorize_hubspot(user_id: str = Form(...), org_id: str = Form(...)):
    """
    Generate the authorization URL for HubSpot OAuth.
    """
    state_data = {
        "state": secrets.token_urlsafe(32),
        "user_id": user_id,
        "org_id": org_id
    }
    encoded_state = base64.urlsafe_b64encode(json.dumps(state_data).encode()).decode()
    await add_key_value_redis(f"hubspot_state:{org_id}:{user_id}", json.dumps(state_data), expire=600)

    # Build authorization URL with updated scopes
    auth_url = (
        f"https://app.hubspot.com/oauth/authorize"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope={SCOPES}"
        f"&state={encoded_state}"
    )
    logging.debug(f"Authorization URL: {auth_url}")  # Debugging log
    return {"auth_url": auth_url}

@router.get("/oauth2callback")
async def oauth2callback_hubspot(request: Request):
    """
    Handle the OAuth callback from HubSpot.
    """
    code = request.query_params.get("code")
    encoded_state = request.query_params.get("state")
    error = request.query_params.get("error") or request.query_params.get("error_description")

    if error:
        raise HTTPException(status_code=400, detail=f"OAuth error: {error}")

    # Decode state
    try:
        state_data = json.loads(base64.urlsafe_b64decode(encoded_state).decode())
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid state format")

    user_id = state_data["user_id"]
    org_id = state_data["org_id"]

    # Validate state
    saved_state = await get_value_redis(f"hubspot_state:{org_id}:{user_id}")
    if not saved_state or state_data["state"] != json.loads(saved_state).get("state"):
        raise HTTPException(status_code=400, detail="Invalid state")

    # Exchange code for tokens
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.hubapi.com/oauth/v1/token",
            data={
                "grant_type": "authorization_code",
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uri": REDIRECT_URI,
                "code": code
            }
        )
        if response.status_code != 200:
            logging.error(f"Token exchange failed: {response.text}")
            raise HTTPException(status_code=400, detail="Failed to fetch tokens")
        credentials = response.json()

    # Store credentials in Redis
    await add_key_value_redis(
        f"hubspot_credentials:{org_id}:{user_id}",
        json.dumps(credentials),
        expire=credentials.get("expires_in", 3600)
    )

    # Close OAuth window
    return HTMLResponse("<script>window.close();</script>")

@router.post("/credentials")
async def get_hubspot_credentials(user_id: str = Form(...), org_id: str = Form(...)):
    """
    Retrieve HubSpot credentials from Redis.
    """
    credentials = await get_value_redis(f"hubspot_credentials:{org_id}:{user_id}")
    if not credentials:
        raise HTTPException(status_code=404, detail="Credentials not found")
    return json.loads(credentials)

@router.post("/load")
async def load_hubspot_items(user_id: str = Form(...), org_id: str = Form(...)):
    """
    Fetch HubSpot contacts, companies, deals, and tickets and convert them into IntegrationItem objects.
    """
    credentials = await get_hubspot_credentials(user_id, org_id)
    items = await get_items_hubspot(credentials)
    return {"items": [item.dict() for item in items]}

async def get_items_hubspot(credentials):
    """
    Fetch HubSpot contacts, companies, deals, and tickets and convert them into IntegrationItem objects.
    """
    access_token = credentials.get("access_token")
    items = []

    async def fetch_and_process(endpoint, object_type, name_key):
        """
        Helper function to fetch data from HubSpot and process it into IntegrationItem objects.
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.hubapi.com/crm/v3/objects/{endpoint}",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            if response.status_code != 200:
                logging.error(f"Failed to fetch {object_type}: {response.text}")
                raise HTTPException(status_code=400, detail=f"Failed to fetch {object_type}")

            results = response.json().get("results", [])
            for obj in results:
                try:
                    creation_time = datetime.fromisoformat(obj["createdAt"].replace("Z", "+00:00"))
                    last_modified_time = datetime.fromisoformat(obj["updatedAt"].replace("Z", "+00:00"))
                except ValueError:
                    logging.error(f"Invalid date format for {object_type} ID: {obj['id']}")
                    raise HTTPException(status_code=400, detail=f"Invalid date format in HubSpot response")

                name = obj['properties'].get(name_key, '').strip()
                items.append(
                    IntegrationItem(
                        id=obj["id"],
                        name=name,
                        type=object_type,
                        creation_time=creation_time,
                        last_modified_time=last_modified_time,
                        parent_id=None
                    )
                )

    # Fetch Contacts
    await fetch_and_process("contacts", "Contact", "firstname")
    # Fetch Companies
    await fetch_and_process("companies", "Company", "name")
    # Fetch Deals
    await fetch_and_process("deals", "Deal", "dealname")
    # Fetch Tickets
    await fetch_and_process("tickets", "Ticket", "subject")

    return items