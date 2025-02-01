# # # # # # from fastapi import FastAPI, Form, Request
# # # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # # from fastapi.staticfiles import StaticFiles

# # # # # # from integrations.airtable import authorize_airtable, get_items_airtable, oauth2callback_airtable, get_airtable_credentials
# # # # # # from integrations.notion import authorize_notion, get_items_notion, oauth2callback_notion, get_notion_credentials
# # # # # # from integrations.hubspot import authorize_hubspot, get_hubspot_credentials, get_items_hubspot, oauth2callback_hubspot

# # # # # # app = FastAPI()

# # # # # # origins = [
# # # # # #     "http://localhost:3000",  # React app address
# # # # # # ]
# # # # # # app.add_middleware(
# # # # # #     CORSMiddleware,
# # # # # #     allow_origins=origins,
# # # # # #     allow_credentials=True,
# # # # # #     allow_methods=["*"],
# # # # # #     allow_headers=["*"],
# # # # # # )

# # # # # # @app.get('/')
# # # # # # def read_root():
# # # # # #     return {'Ping': 'Pong'}


# # # # # # # Airtable
# # # # # # @app.post('/integrations/airtable/authorize')
# # # # # # async def authorize_airtable_integration(user_id: str = Form(...), org_id: str = Form(...)):
# # # # # #     return await authorize_airtable(user_id, org_id)

# # # # # # @app.get('/integrations/airtable/oauth2callback')
# # # # # # async def oauth2callback_airtable_integration(request: Request):
# # # # # #     return await oauth2callback_airtable(request)

# # # # # # @app.post('/integrations/airtable/credentials')
# # # # # # async def get_airtable_credentials_integration(user_id: str = Form(...), org_id: str = Form(...)):
# # # # # #     return await get_airtable_credentials(user_id, org_id)

# # # # # # @app.post('/integrations/airtable/load')
# # # # # # async def get_airtable_items(credentials: str = Form(...)):
# # # # # #     return await get_items_airtable(credentials)


# # # # # # # Notion
# # # # # # @app.post('/integrations/notion/authorize')
# # # # # # async def authorize_notion_integration(user_id: str = Form(...), org_id: str = Form(...)):
# # # # # #     return await authorize_notion(user_id, org_id)

# # # # # # @app.get('/integrations/notion/oauth2callback')
# # # # # # async def oauth2callback_notion_integration(request: Request):
# # # # # #     return await oauth2callback_notion(request)

# # # # # # @app.post('/integrations/notion/credentials')
# # # # # # async def get_notion_credentials_integration(user_id: str = Form(...), org_id: str = Form(...)):
# # # # # #     return await get_notion_credentials(user_id, org_id)

# # # # # # @app.post('/integrations/notion/load')
# # # # # # async def get_notion_items(credentials: str = Form(...)):
# # # # # #     return await get_items_notion(credentials)

# # # # # # # HubSpot
# # # # # # @app.post('/integrations/hubspot/authorize')
# # # # # # async def authorize_hubspot_integration(user_id: str = Form(...), org_id: str = Form(...)):
# # # # # #     return await authorize_hubspot(user_id, org_id)

# # # # # # @app.get('/integrations/hubspot/oauth2callback')
# # # # # # async def oauth2callback_hubspot_integration(request: Request):
# # # # # #     return await oauth2callback_hubspot(request)

# # # # # # @app.post('/integrations/hubspot/credentials')
# # # # # # async def get_hubspot_credentials_integration(user_id: str = Form(...), org_id: str = Form(...)):
# # # # # #     return await get_hubspot_credentials(user_id, org_id)

# # # # # # @app.post('/integrations/hubspot/get_hubspot_items')
# # # # # # async def load_slack_data_integration(credentials: str = Form(...)):
# # # # # #     return await get_items_hubspot(credentials)
# # from fastapi import FastAPI, Form, Request
# # from fastapi.middleware.cors import CORSMiddleware
# # from integrations.airtable import authorize_airtable, get_items_airtable, oauth2callback_airtable, get_airtable_credentials
# # from integrations.notion import authorize_notion, get_items_notion, oauth2callback_notion, get_notion_credentials
# # from integrations.hubspot import authorize_hubspot, get_hubspot_credentials, get_items_hubspot, oauth2callback_hubspot
# # from dotenv import load_dotenv
# # import os

# # # Load environment variables from .env file
# # load_dotenv()
# # app = FastAPI()

# # # CORS Configuration
# # origins = [
# #     "http://localhost:3000",  # React app address
# # ]

# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=origins,
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # @app.get('/')
# # def read_root():
# #     return {'Ping': 'Pong'}

# # # Airtable Routes
# # @app.post('/integrations/airtable/authorize')
# # async def authorize_airtable_integration(user_id: str = Form(...), org_id: str = Form(...)):
# #     return await authorize_airtable(user_id, org_id)

# # @app.get('/integrations/airtable/oauth2callback')
# # async def oauth2callback_airtable_integration(request: Request):
# #     return await oauth2callback_airtable(request)

# # @app.post('/integrations/airtable/credentials')
# # async def get_airtable_credentials_integration(user_id: str = Form(...), org_id: str = Form(...)):
# #     return await get_airtable_credentials(user_id, org_id)

# # @app.post('/integrations/airtable/load')
# # async def get_airtable_items(credentials: str = Form(...)):
# #     return await get_items_airtable(credentials)

# # # Notion Routes
# # @app.post('/integrations/notion/authorize')
# # async def authorize_notion_integration(user_id: str = Form(...), org_id: str = Form(...)):
# #     return await authorize_notion(user_id, org_id)

# # @app.get('/integrations/notion/oauth2callback')
# # async def oauth2callback_notion_integration(request: Request):
# #     return await oauth2callback_notion(request)

# # @app.post('/integrations/notion/credentials')
# # async def get_notion_credentials_integration(user_id: str = Form(...), org_id: str = Form(...)):
# #     return await get_notion_credentials(user_id, org_id)

# # @app.post('/integrations/notion/load')
# # async def get_notion_items(credentials: str = Form(...)):
# #     return await get_items_notion(credentials)

# # # HubSpot Routes
# # @app.post('/integrations/hubspot/authorize')
# # async def authorize_hubspot_integration(user_id: str = Form(...), org_id: str = Form(...)):
# #     auth_url = await authorize_hubspot(user_id, org_id)
# #     return {"auth_url": auth_url}  # Return the authorization URL as JSON

# # @app.get('/integrations/hubspot/oauth2callback')
# # async def oauth2callback_hubspot_integration(request: Request):
# #     return await oauth2callback_hubspot(request)

# # @app.post('/integrations/hubspot/credentials')
# # async def get_hubspot_credentials_integration(user_id: str = Form(...), org_id: str = Form(...)):
# #     credentials = await get_hubspot_credentials(user_id, org_id)
# #     return credentials  # Return the credentials directly

# # @app.post('/integrations/hubspot/load')
# # async def load_hubspot_items(user_id: str = Form(...), org_id: str = Form(...)):
# #     credentials = await get_hubspot_credentials(user_id, org_id)
# #     items = await get_items_hubspot(credentials)
# #     return {"items": [item.dict() for item in items]}  # Return the list of IntegrationItem objects
# from fastapi import FastAPI, Form, Request
# from fastapi.middleware.cors import CORSMiddleware
# from dotenv import load_dotenv
# from integrations.hubspot import router as hubspot_router

# # Import integration functions
# from integrations.airtable import (
#     authorize_airtable, get_items_airtable, oauth2callback_airtable, get_airtable_credentials
# )
# from integrations.notion import (
#     authorize_notion, get_items_notion, oauth2callback_notion, get_notion_credentials
# )
# from integrations.hubspot import (
#     authorize_hubspot, get_hubspot_credentials, get_items_hubspot, oauth2callback_hubspot
# )

# # Load environment variables
# load_dotenv()

# # Initialize FastAPI app
# app = FastAPI()

# # CORS Configuration
# origins = ["http://localhost:3000"]  # Adjust as needed

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# app.include_router(hubspot_router, prefix="/integrations/hubspot")

# @app.get('/')
# def read_root():
#     return {"Ping": "Pong"}

# # Airtable Routes
# @app.post('/integrations/airtable/authorize')
# async def authorize_airtable_integration(user_id: str = Form(...), org_id: str = Form(...)):
#     return await authorize_airtable(user_id, org_id)

# @app.get('/integrations/airtable/oauth2callback')
# async def oauth2callback_airtable_integration(request: Request):
#     return await oauth2callback_airtable(request)

# @app.post('/integrations/airtable/credentials')
# async def get_airtable_credentials_integration(user_id: str = Form(...), org_id: str = Form(...)):
#     return await get_airtable_credentials(user_id, org_id)

# @app.post('/integrations/airtable/load')
# async def get_airtable_items(credentials: str = Form(...)):
#     return await get_items_airtable(credentials)

# # Notion Routes
# @app.post('/integrations/notion/authorize')
# async def authorize_notion_integration(user_id: str = Form(...), org_id: str = Form(...)):
#     return await authorize_notion(user_id, org_id)

# @app.get('/integrations/notion/oauth2callback')
# async def oauth2callback_notion_integration(request: Request):
#     return await oauth2callback_notion(request)

# @app.post('/integrations/notion/credentials')
# async def get_notion_credentials_integration(user_id: str = Form(...), org_id: str = Form(...)):
#     return await get_notion_credentials(user_id, org_id)

# @app.post('/integrations/notion/load')
# async def get_notion_items(credentials: str = Form(...)):
#     return await get_items_notion(credentials)

# # HubSpot Routes
# @app.post('/integrations/hubspot/authorize')
# async def authorize_hubspot_integration(user_id: str = Form(...), org_id: str = Form(...)):
#     auth_url = await authorize_hubspot(user_id, org_id)
#     return {"auth_url": auth_url}

# @app.get('/integrations/hubspot/oauth2callback')
# async def oauth2callback_hubspot_integration(request: Request):
#     return await oauth2callback_hubspot(request)

# @app.post('/integrations/hubspot/credentials')
# async def get_hubspot_credentials_integration(user_id: str = Form(...), org_id: str = Form(...)):
#     credentials = await get_hubspot_credentials(user_id, org_id)
#     return credentials

# @app.post('/integrations/hubspot/load')
# async def load_hubspot_items(user_id: str = Form(...), org_id: str = Form(...)):
#     credentials = await get_hubspot_credentials(user_id, org_id)
#     items = await get_items_hubspot(credentials)
#     return {"items": [item.dict() for item in items]}
from fastapi import FastAPI, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from integrations.hubspot import router as hubspot_router  # Import the router
from integrations.airtable import authorize_airtable, get_items_airtable, oauth2callback_airtable, get_airtable_credentials
from integrations.notion import authorize_notion, get_items_notion, oauth2callback_notion, get_notion_credentials
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
app = FastAPI()

# CORS Configuration
origins = [
    "http://localhost:3000",  # React app address
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the HubSpot router
app.include_router(hubspot_router, prefix="/integrations/hubspot", tags=["HubSpot"])

@app.get('/')
def read_root():
    return {'Ping': 'Pong'}

# Airtable Routes
@app.post('/integrations/airtable/authorize')
async def authorize_airtable_integration(user_id: str = Form(...), org_id: str = Form(...)):
    return await authorize_airtable(user_id, org_id)

@app.get('/integrations/airtable/oauth2callback')
async def oauth2callback_airtable_integration(request: Request):
    return await oauth2callback_airtable(request)

@app.post('/integrations/airtable/credentials')
async def get_airtable_credentials_integration(user_id: str = Form(...), org_id: str = Form(...)):
    return await get_airtable_credentials(user_id, org_id)

@app.post('/integrations/airtable/load')
async def get_airtable_items(credentials: str = Form(...)):
    return await get_items_airtable(credentials)

# Notion Routes
@app.post('/integrations/notion/authorize')
async def authorize_notion_integration(user_id: str = Form(...), org_id: str = Form(...)):
    return await authorize_notion(user_id, org_id)

@app.get('/integrations/notion/oauth2callback')
async def oauth2callback_notion_integration(request: Request):
    return await oauth2callback_notion(request)

@app.post('/integrations/notion/credentials')
async def get_notion_credentials_integration(user_id: str = Form(...), org_id: str = Form(...)):
    return await get_notion_credentials(user_id, org_id)

@app.post('/integrations/notion/load')
async def get_notion_items(credentials: str = Form(...)):
    return await get_items_notion(credentials)