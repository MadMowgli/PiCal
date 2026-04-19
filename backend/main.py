from datetime import datetime
import json
from contextlib import asynccontextmanager

from fastapi import FastAPI
from googleapiclient.discovery import build

import auth_handler


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.credentials = auth_handler.get_credentials()
    app.state.service = build("calendar", "v3", credentials=app.state.credentials)
    with open('config.json', 'r') as config_file:
        app.state.config = json.load(config_file)

    yield


app = FastAPI(lifespan=lifespan)


@app.get('/events')
async def get_calendar():

    # Get last 50 events from calendar
    events = app.state.service.events().list(
        calendarId=app.state.config['calendarId'],
        maxResults=50
    ).execute()

    # Filter out timed events
    timed_events = [
        {
            'Start': x['start']['dateTime'],
            'End': x['end']['dateTime'],
            'Creator': x['creator'],
            'Summary': x['summary']
        } for x in events['items'] if 'dateTime' in x['start']
    ]

    # Also get all day events
    all_day_events = [
        {
            'Start': x['start']['date'],
            'End': x['end']['date'],
            'Creator': x['creator'],
            'Summary': x['summary']
        } for x in events['items'] if 'dateTime' not in x['start']

    ]

    # Merge all events, sort them by datetime
    all_events = all_day_events + timed_events
    all_events.sort(key=lambda x: x['Start'])

    # Format the datetime of each event to make it more readable
    for event in all_events:
        event['Start'] = datetime.fromisoformat(event['Start']).strftime('%d.%m.%Y %H:%M:%S')
        event['End'] = datetime.fromisoformat(event['End']).strftime('%d.%m.%Y %H:%M:%S')

    return all_events


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
