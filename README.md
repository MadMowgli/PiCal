# PiCal

A FastAPI backend for a Raspberry Pi home dashboard. Pulls calendar data from Google Calendar and exposes it via REST API. Weather and SBB train information will follow.

## Authentication Workflow

The app uses Google OAuth 2.0 with read-only calendar access. On first run, it opens a browser for you to authenticate with your Google account. After that, the token is cached in `token.json` and refreshed automatically.
If the token expires and can't be refreshed, the browser flow is triggered again. On a headless Pi, the initial authentication must happen on a machine with a browser -- copy the resulting `token.json` to the Pi afterwards.

## Prerequisites

1. A Google Cloud project with the Calendar API enabled.
2. OAuth 2.0 credentials downloaded as `client_secret.json` in the project root.
3. A `config.json` in the project root:
   ```json
   {
     "calendarId": "your-calendar-id@group.calendar.google.com"
   }
   ```
4. Python 3.14 with dependencies installed:
   ```
   pip install fastapi uvicorn google-api-python-client google-auth-oauthlib
   ```
5. Run the app:
   ```
   uvicorn main:app
   ```
