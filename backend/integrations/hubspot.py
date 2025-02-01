# # # # # # # # # hubspot.py

# # # # # # # # import json
# # # # # # # # import secrets
# # # # # # # # import base64
# # # # # # # # from fastapi import Request, HTTPException
# # # # # # # # from fastapi.responses import HTMLResponse
# # # # # # # # import httpx
# # # # # # # # import asyncio
# # # # # # # # from integrations.integration_item import IntegrationItem
# # # # # # # # from redis_client import add_key_value_redis, get_value_redis, delete_key_redis

# # # # # # # # # HubSpot OAuth Credentials (Replace with your app's credentials)
# # # # # # # # CLIENT_ID = "d54b6e66-7500-43ad-8e08-be4aa3ef40f6"
# # # # # # # # CLIENT_SECRET = "5a7cd1ac-6095-4f32-af87-701140cd9cac"
# # # # # # # # REDIRECT_URI = "http://localhost:8000/integrations/hubspot/oauth2callback"
# # # # # # # # ENCODED_CLIENT_CREDENTIALS = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()

# # # # # # # # async def authorize_hubspot(user_id, org_id):
# # # # # # # #     # Generate state and store in Redis
# # # # # # # #     state_data = {
# # # # # # # #         "state": secrets.token_urlsafe(32),
# # # # # # # #         "user_id": user_id,
# # # # # # # #         "org_id": org_id
# # # # # # # #     }
# # # # # # # #     encoded_state = base64.urlsafe_b64encode(json.dumps(state_data).encode()).decode()
    
# # # # # # # #     # Store state in Redis
# # # # # # # #     await add_key_value_redis(f"hubspot_state:{org_id}:{user_id}", json.dumps(state_data), expire=600)
    
# # # # # # # #     # Build authorization URL
# # # # # # # #     auth_url = (
# # # # # # # #         f"https://app.hubspot.com/oauth/authorize"
# # # # # # # #         f"?client_id={CLIENT_ID}"
# # # # # # # #         f"&redirect_uri={REDIRECT_URI}"
# # # # # # # #         f"&scope=contacts"
# # # # # # # #         f"&state={encoded_state}"
# # # # # # # #     )
# # # # # # # #     return auth_url

# # # # # # # # async def oauth2callback_hubspot(request: Request):
# # # # # # # #     # Handle OAuth callback
# # # # # # # #     code = request.query_params.get("code")
# # # # # # # #     encoded_state = request.query_params.get("state")
# # # # # # # #     error = request.query_params.get("error")
    
# # # # # # # #     if error:
# # # # # # # #         raise HTTPException(status_code=400, detail=f"OAuth error: {error}")
    
# # # # # # # #     # Decode state
# # # # # # # #     state_data = json.loads(base64.urlsafe_b64decode(encoded_state).decode())
# # # # # # # #     user_id = state_data["user_id"]
# # # # # # # #     org_id = state_data["org_id"]
    
# # # # # # # #     # Validate state
# # # # # # # #     saved_state = await get_value_redis(f"hubspot_state:{org_id}:{user_id}")
# # # # # # # #     if not saved_state or state_data["state"] != json.loads(saved_state).get("state"):
# # # # # # # #         raise HTTPException(status_code=400, detail="Invalid state")
    
# # # # # # # #     # Exchange code for tokens
# # # # # # # #     async with httpx.AsyncClient() as client:
# # # # # # # #         response = await client.post(
# # # # # # # #             "https://api.hubapi.com/oauth/v1/token",
# # # # # # # #             data={
# # # # # # # #                 "grant_type": "authorization_code",
# # # # # # # #                 "client_id": CLIENT_ID,
# # # # # # # #                 "client_secret": CLIENT_SECRET,
# # # # # # # #                 "redirect_uri": REDIRECT_URI,
# # # # # # # #                 "code": code
# # # # # # # #             }
# # # # # # # #         )
# # # # # # # #         if response.status_code != 200:
# # # # # # # #             raise HTTPException(status_code=400, detail="Failed to fetch tokens")
        
# # # # # # # #         credentials = response.json()
    
# # # # # # # #     # Store credentials in Redis
# # # # # # # #     await add_key_value_redis(
# # # # # # # #         f"hubspot_credentials:{org_id}:{user_id}",
# # # # # # # #         json.dumps(credentials),
# # # # # # # #         expire=credentials.get("expires_in", 3600)
# # # # # # # #     )
    
# # # # # # # #     # Close OAuth window
# # # # # # # #     return HTMLResponse("<script>window.close()</script>")

# # # # # # # # async def get_hubspot_credentials(user_id, org_id):
# # # # # # # #     # Retrieve credentials from Redis
# # # # # # # #     credentials = await get_value_redis(f"hubspot_credentials:{org_id}:{user_id}")
# # # # # # # #     if not credentials:
# # # # # # # #         raise HTTPException(status_code=404, detail="Credentials not found")
# # # # # # # #     return json.loads(credentials)

# # # # # # # # async def get_items_hubspot(credentials):
# # # # # # # #     # Fetch HubSpot contacts
# # # # # # # #     access_token = credentials.get("access_token")
# # # # # # # #     async with httpx.AsyncClient() as client:
# # # # # # # #         response = await client.get(
# # # # # # # #             "https://api.hubapi.com/crm/v3/objects/contacts",
# # # # # # # #             headers={"Authorization": f"Bearer {access_token}"}
# # # # # # # #         )
# # # # # # # #         if response.status_code != 200:
# # # # # # # #             raise HTTPException(status_code=400, detail="Failed to fetch contacts")
        
# # # # # # # #         contacts = response.json().get("results", [])
    
# # # # # # # #     # Convert to IntegrationItem objects
# # # # # # # #     items = []
# # # # # # # #     for contact in contacts:
# # # # # # # #         items.append(
# # # # # # # #             IntegrationItem(
# # # # # # # #                 id=contact["id"],
# # # # # # # #                 name=contact["properties"].get("firstname", "") + " " + contact["properties"].get("lastname", ""),
# # # # # # # #                 type="Contact",
# # # # # # # #                 creation_time=contact["createdAt"],
# # # # # # # #                 last_modified_time=contact["updatedAt"]
# # # # # # # #             )
# # # # # # # #         )
# # # # # # # #     return items
# # # # # # # # hubspot.py
# # import json
# # import secrets
# # from datetime import datetime
# # from fastapi import Request, HTTPException
# # from fastapi.responses import HTMLResponse
# # import httpx
# # import os
# # import base64  # Add this import
# # from integrations.integration_item import IntegrationItem
# # from redis_client import add_key_value_redis, get_value_redis, delete_key_redis

# # # HubSpot OAuth Credentials
# # CLIENT_ID = os.getenv("HUBSPOT_CLIENT_ID")
# # CLIENT_SECRET = os.getenv("HUBSPOT_CLIENT_SECRET")
# # REDIRECT_URI = "http://localhost:8000/integrations/hubspot/oauth2callback"
# # SCOPES = "crm.objects.contacts.read crm.objects.contacts.write crm.objects.companies.read crm.objects.deals.read oauth"

# # async def authorize_hubspot(user_id, org_id):
# #     """
# #     Generate the authorization URL for HubSpot OAuth.
# #     """
# #     state_data = {
# #         "state": secrets.token_urlsafe(32),
# #         "user_id": user_id,
# #         "org_id": org_id
# #     }
# #     encoded_state = base64.urlsafe_b64encode(json.dumps(state_data).encode()).decode()
# #     await add_key_value_redis(f"hubspot_state:{org_id}:{user_id}", json.dumps(state_data), expire=600)

# #     # Build authorization URL
# #     auth_url = (
# #         f"https://app.hubspot.com/oauth/authorize"
# #         f"?client_id={CLIENT_ID}"
# #         f"&redirect_uri={REDIRECT_URI}"
# #         f"&scope={SCOPES}"
# #         f"&state={encoded_state}"
# #     )
# #     return auth_url


# # async def oauth2callback_hubspot(request: Request):
# #     """
# #     Handle the OAuth callback from HubSpot.
# #     """
# #     code = request.query_params.get("code")
# #     encoded_state = request.query_params.get("state")
# #     error = request.query_params.get("error") or request.query_params.get("error_description")

# #     if error:
# #         raise HTTPException(status_code=400, detail=f"OAuth error: {error}")

# #     # Decode state
# #     try:
# #         state_data = json.loads(base64.urlsafe_b64decode(encoded_state).decode())
# #     except Exception:
# #         raise HTTPException(status_code=400, detail="Invalid state format")

# #     user_id = state_data["user_id"]
# #     org_id = state_data["org_id"]

# #     # Validate state
# #     saved_state = await get_value_redis(f"hubspot_state:{org_id}:{user_id}")
# #     if not saved_state or state_data["state"] != json.loads(saved_state).get("state"):
# #         raise HTTPException(status_code=400, detail="Invalid state")

# #     # Exchange code for tokens
# #     async with httpx.AsyncClient() as client:
# #         response = await client.post(
# #             "https://api.hubapi.com/oauth/v1/token",
# #             data={
# #                 "grant_type": "authorization_code",
# #                 "client_id": CLIENT_ID,
# #                 "client_secret": CLIENT_SECRET,
# #                 "redirect_uri": REDIRECT_URI,
# #                 "code": code
# #             }
# #         )
# #         if response.status_code != 200:
# #             raise HTTPException(status_code=400, detail="Failed to fetch tokens")
# #         credentials = response.json()

# #     # Store credentials in Redis
# #     await add_key_value_redis(
# #         f"hubspot_credentials:{org_id}:{user_id}",
# #         json.dumps(credentials),
# #         expire=credentials.get("expires_in", 3600)
# #     )

# #     # Close OAuth window
# #     return HTMLResponse("<script>window.close();</script>")


# # async def get_hubspot_credentials(user_id, org_id):
# #     """
# #     Retrieve HubSpot credentials from Redis.
# #     """
# #     credentials = await get_value_redis(f"hubspot_credentials:{org_id}:{user_id}")
# #     if not credentials:
# #         raise HTTPException(status_code=404, detail="Credentials not found")
# #     return json.loads(credentials)


# # async def get_items_hubspot(credentials):
# #     """
# #     Fetch HubSpot contacts and convert them into IntegrationItem objects.
# #     """
# #     access_token = credentials.get("access_token")
# #     async with httpx.AsyncClient() as client:
# #         response = await client.get(
# #             "https://api.hubapi.com/crm/v3/objects/contacts",
# #             headers={"Authorization": f"Bearer {access_token}"}
# #         )
# #         if response.status_code != 200:
# #             raise HTTPException(status_code=400, detail="Failed to fetch contacts")
# #         contacts = response.json().get("results", [])

# #     items = []
# #     for contact in contacts:
# #         # Convert creation_time and last_modified_time to datetime objects
# #         try:
# #             creation_time = datetime.fromisoformat(contact["createdAt"].replace("Z", "+00:00"))
# #             last_modified_time = datetime.fromisoformat(contact["updatedAt"].replace("Z", "+00:00"))
# #         except ValueError:
# #             raise HTTPException(status_code=400, detail="Invalid date format in HubSpot response")

# #         items.append(
# #             IntegrationItem(
# #                 id=contact["id"],
# #                 name=f"{contact['properties'].get('firstname', '')} {contact['properties'].get('lastname', '')}".strip(),
# #                 type="Contact",
# #                 creation_time=creation_time,
# #                 last_modified_time=last_modified_time
# #             )
# #         )
# #     return items
# import json
# import secrets
# from datetime import datetime
# from fastapi import Request, HTTPException
# from fastapi.responses import HTMLResponse
# import httpx
# import os
# import base64
# from integrations.integration_item import IntegrationItem
# from redis_client import add_key_value_redis, get_value_redis, delete_key_redis
# import logging

# logging.basicConfig(level=logging.DEBUG)

# # HubSpot OAuth Credentials
# # CLIENT_ID = os.getenv("HUBSPOT_CLIENT_ID")
# # CLIENT_SECRET = os.getenv("HUBSPOT_CLIENT_SECRET")
# CLIENT_ID = "64c81a4b-dcb5-4c4f-a751-f79a464633c0"
# CLIENT_SECRET = "b557bbbd-7694-489e-9ae6-8a8ede7c8746"
# REDIRECT_URI = "http://localhost:8000/integrations/hubspot/oauth2callback"
# SCOPES = "crm.objects.contacts.read crm.objects.contacts.write crm.objects.companies.read crm.objects.deals.read oauth"

# # Debugging: Print environment variables
# print(f"CLIENT_ID: {CLIENT_ID}")
# print(f"CLIENT_SECRET: {CLIENT_SECRET}")

# async def authorize_hubspot(user_id, org_id):
#     """
#     Generate the authorization URL for HubSpot OAuth.
#     """
#     state_data = {
#         "state": secrets.token_urlsafe(32),
#         "user_id": user_id,
#         "org_id": org_id
#     }
#     encoded_state = base64.urlsafe_b64encode(json.dumps(state_data).encode()).decode()
#     await add_key_value_redis(f"hubspot_state:{org_id}:{user_id}", json.dumps(state_data), expire=600)

#     # Build authorization URL
#     auth_url = (
#         f"https://app.hubspot.com/oauth/authorize"
#         f"?client_id={CLIENT_ID}"
#         f"&redirect_uri={REDIRECT_URI}"
#         f"&scope={SCOPES}"
#         f"&state={encoded_state}"
#     )
#     return auth_url

# async def oauth2callback_hubspot(request: Request):
#     """
#     Handle the OAuth callback from HubSpot.
#     """
#     code = request.query_params.get("code")
#     encoded_state = request.query_params.get("state")
#     error = request.query_params.get("error") or request.query_params.get("error_description")

#     if error:
#         raise HTTPException(status_code=400, detail=f"OAuth error: {error}")

#     # Decode state
#     try:
#         state_data = json.loads(base64.urlsafe_b64decode(encoded_state).decode())
#     except Exception:
#         raise HTTPException(status_code=400, detail="Invalid state format")

#     user_id = state_data["user_id"]
#     org_id = state_data["org_id"]

#     # Validate state
#     saved_state = await get_value_redis(f"hubspot_state:{org_id}:{user_id}")
#     if not saved_state or state_data["state"] != json.loads(saved_state).get("state"):
#         raise HTTPException(status_code=400, detail="Invalid state")

#     # Exchange code for tokens
#     async with httpx.AsyncClient() as client:
#         response = await client.post(
#             "https://api.hubapi.com/oauth/v1/token",
#             data={
#                 "grant_type": "authorization_code",
#                 "client_id": CLIENT_ID,
#                 "client_secret": CLIENT_SECRET,
#                 "redirect_uri": REDIRECT_URI,
#                 "code": code
#             }
#         )
#         if response.status_code != 200:
#             raise HTTPException(status_code=400, detail="Failed to fetch tokens")
#         credentials = response.json()

#     # Store credentials in Redis
#     await add_key_value_redis(
#         f"hubspot_credentials:{org_id}:{user_id}",
#         json.dumps(credentials),
#         expire=credentials.get("expires_in", 3600)
#     )

#     # Close OAuth window
#     return HTMLResponse("<script>window.close();</script>")

# async def get_hubspot_credentials(user_id, org_id):
#     """
#     Retrieve HubSpot credentials from Redis.
#     """
#     credentials = await get_value_redis(f"hubspot_credentials:{org_id}:{user_id}")
#     if not credentials:
#         raise HTTPException(status_code=404, detail="Credentials not found")
#     return json.loads(credentials)

# async def get_items_hubspot(credentials):
#     """
#     Fetch HubSpot contacts and convert them into IntegrationItem objects.
#     """
#     access_token = credentials.get("access_token")
#     async with httpx.AsyncClient() as client:
#         response = await client.get(
#             "https://api.hubapi.com/crm/v3/objects/contacts",
#             headers={"Authorization": f"Bearer {access_token}"}
#         )
#         if response.status_code != 200:
#             raise HTTPException(status_code=400, detail="Failed to fetch contacts")
#         contacts = response.json().get("results", [])

#     items = []
#     for contact in contacts:
#         # Convert creation_time and last_modified_time to datetime objects
#         try:
#             creation_time = datetime.fromisoformat(contact["createdAt"].replace("Z", "+00:00"))
#             last_modified_time = datetime.fromisoformat(contact["updatedAt"].replace("Z", "+00:00"))
#         except ValueError:
#             raise HTTPException(status_code=400, detail="Invalid date format in HubSpot response")

#         items.append(
#             IntegrationItem(
#                 id=contact["id"],
#                 name=f"{contact['properties'].get('firstname', '')} {contact['properties'].get('lastname', '')}".strip(),
#                 type="Contact",
#                 creation_time=creation_time,
#                 last_modified_time=last_modified_time
#             )
#         )
#     return items
import json
import secrets
from datetime import datetime
from fastapi import Request, HTTPException
from fastapi.responses import HTMLResponse
import httpx
import os
import base64
from integrations.integration_item import IntegrationItem
from redis_client import add_key_value_redis, get_value_redis, delete_key_redis
import logging

logging.basicConfig(level=logging.DEBUG)

# HubSpot OAuth Credentials
# CLIENT_ID = "64c81a4b-dcb5-4c4f-a751-f79a464633c0"
# CLIENT_SECRET = "b557bbbd-7694-489e-9ae6-8a8ede7c8746"
REDIRECT_URI = "http://localhost:8000/integrations/hubspot/oauth2callback"
SCOPES = "crm.objects.contacts.read crm.objects.contacts.write crm.objects.companies.read crm.objects.deals.read oauth"

# Debugging: Print environment variables
print(f"CLIENT_ID: {CLIENT_ID}")
print(f"CLIENT_SECRET: {CLIENT_SECRET}")

async def authorize_hubspot(user_id, org_id):
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

    # Build authorization URL
    auth_url = (
        f"https://app.hubspot.com/oauth/authorize"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope={SCOPES}"
        f"&state={encoded_state}"
    )
    return auth_url

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

async def get_hubspot_credentials(user_id, org_id):
    """
    Retrieve HubSpot credentials from Redis.
    """
    credentials = await get_value_redis(f"hubspot_credentials:{org_id}:{user_id}")
    if not credentials:
        raise HTTPException(status_code=404, detail="Credentials not found")
    return json.loads(credentials)

async def get_items_hubspot(credentials):
    """
    Fetch HubSpot contacts and convert them into IntegrationItem objects.
    """
    access_token = credentials.get("access_token")
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.hubapi.com/crm/v3/objects/contacts",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch contacts")
        contacts = response.json().get("results", [])

    items = []
    for contact in contacts:
        # Convert creation_time and last_modified_time to datetime objects
        try:
            creation_time = datetime.fromisoformat(contact["createdAt"].replace("Z", "+00:00"))
            last_modified_time = datetime.fromisoformat(contact["updatedAt"].replace("Z", "+00:00"))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format in HubSpot response")

        items.append(
            IntegrationItem(
                id=contact["id"],
                name=f"{contact['properties'].get('firstname', '')} {contact['properties'].get('lastname', '')}".strip(),
                type="Contact",
                creation_time=creation_time,
                last_modified_time=last_modified_time
            )
        )
    return items