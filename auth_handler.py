import json
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


TOKEN_FILE = "token.json"
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

def get_credentials():
    credentials = None

    # Load cached token if it exists
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            credentials = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # If no or invalid creds, auth
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(TOKEN_FILE, SCOPES)
            credentials = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as f:
            f.write(credentials.to_json())

    return credentials
