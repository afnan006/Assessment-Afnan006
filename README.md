# HubSpot Integration Technical Assessment

This repository contains a full-stack application demonstrating OAuth integration with HubSpot, including credential management and data fetching. Below is a detailed guide to understand, run, and validate the implementation.

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Prerequisites](#prerequisites)
3. [Setup & Installation](#setup--installation)
4. [Running the Application](#running-the-application)
5. [Testing the Integration](#testing-the-integration)
6. [Project Structure](#project-structure)
7. [Implementation Details](#implementation-details)
8. [Screenshots/Demo](#screenshotsdemo)
9. [Troubleshooting](#troubleshooting)

---

## Project Overview
### What Was Built
1. **HubSpot OAuth Integration**  
   - Backend: OAuth 2.0 flow with state management, token exchange, and credential storage using Redis.
   - Frontend: Authorization popup, credential retrieval, and UI status updates.
2. **HubSpot Data Fetching**  
   - Backend: Fetches Contacts, Companies, Deals, and Tickets from HubSpot and converts them into standardized `IntegrationItem` objects.
   - Frontend: Displays fetched items in a list format.

### Key Features
- Secure OAuth flow with PKCE (Proof Key for Code Exchange).
- Redis-based session management for credentials and state.
- Error handling for API failures and invalid states.
- UI consistency with existing Airtable/Notion integrations.

---

## Prerequisites
- **Python 3.9+** (Backend)
- **Node.js v16+** (Frontend)
- **Redis Server** (Local instance)
- **HubSpot Developer Account** ([Create a test app](https://developers.hubspot.com/))
- Environment Variables (See [Setup](#setup--installation))

---

## Setup & Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/afnan006/Assessment-Afnan006.git]
cd afnan006-assessment-afnan006
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

#### Environment Variables (.env)
Create a .env file in /backend with:
```ini
REDIS_HOST=localhost
HUBSPOT_CLIENT_ID=your-hubspot-client-id
HUBSPOT_CLIENT_SECRET=your-hubspot-client-secret
```

### 3. Frontend Setup
```bash
cd ../frontend
npm install
```

## Running the Application

### 1. Start Redis
```bash
redis-server
```

### 2. Start Backend (FastAPI)
```bash
cd backend
uvicorn main:app --reload
```
API Docs: http://localhost:8000/docs

### 3. Start Frontend (React)
```bash
cd frontend
npm start
```
UI: http://localhost:3000

## Testing the Integration

### 1. HubSpot OAuth Flow
1. Open http://localhost:3000
2. Select HubSpot from the "Integration Type" dropdown
3. Click Connect to HubSpot
4. A popup will redirect to HubSpot's OAuth screen. Log in with test credentials
5. After authorization, the popup closes, and the UI shows "HubSpot Connected"

### 2. Fetch HubSpot Items
After connecting, the UI automatically fetches and displays:
- Contacts
- Companies
- Deals
- Tickets

Example Output: HubSpot Items List

### 3. Backend Tests
```bash
cd test
pytest test_hubspot.py -v
```
Validates authorization and data loading logic.

## Project Structure
```
backend/
├── integrations/
│   ├── hubspot.py       # HubSpot OAuth and data fetching logic
│   ├── integration_item.py  # Data model
├── main.py              # FastAPI app and routes
├── redis_client.py      # Redis connection helpers

frontend/
├── src/
│   ├── integrations/
│   │   ├── hubspot.js   # HubSpot UI component
│   ├── integration-form.js  # Integration selector
│   ├── data-form.js     # Data display component
```

## Implementation Details

### Backend (HubSpot OAuth)

#### Authorization
- Generates OAuth URL with state (stored in Redis) and PKCE code_verifier
- Uses HubSpot's /oauth/authorize endpoint

#### Callback Handling
- Validates state against Redis
- Exchanges authorization code for tokens via /oauth/v1/token

#### Credential Storage
- Tokens stored in Redis with expiration matching HubSpot's expires_in

### Backend (Data Fetching)

#### get_items_hubspot method:
- Queries HubSpot's CRM API endpoints (/crm/v3/objects/contacts, etc.)
- Maps results to IntegrationItem with:
  - id: HubSpot object ID
  - name: Contact name/Company name/Deal name
  - type: "Contact", "Company", etc.
  - Timestamps (creation_time, last_modified_time)

### Frontend

#### hubspot.js:
- Opens OAuth popup and polls for closure
- Fetches credentials post-authorization
- Displays fetched items in a scrollable list
- Error handling with MUI components

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Redis connection failed | Ensure redis-server is running |
| Invalid OAuth credentials | Verify .env matches HubSpot app credentials |
| CORS errors | Confirm backend is allowing http://localhost:3000 |
| No items displayed | Check HubSpot test account for dummy data |