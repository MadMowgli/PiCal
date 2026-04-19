# PiCal

A FastAPI backend for a Raspberry Pi home dashboard. Pulls calendar data from Google Calendar and exposes it via REST API. Weather and SBB train information will follow.

## Hardware

- Raspberry Pi (non-headless, running a desktop environment with a browser)
- WaveShare 7.9inch HDMI Capacitive Touch Display (400x1280, portrait-oriented)

## Authentication Workflow

The app uses Google OAuth 2.0 with read-only calendar access. On first run, it opens a browser for you to authenticate with your Google account. After that, the token is cached in `token.json` and refreshed automatically.
If the token expires and can't be refreshed, the browser flow is triggered again. Since the Pi runs a desktop environment with a browser, the OAuth flow can be completed directly on the device.

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
