from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import datetime
from collections import defaultdict
import random
import jdatetime
from datetime import timedelta
import webbrowser
import pytz  # Make sure to import pytz at the top of your file



app = Flask(__name__)
app.secret_key = '9A3F7C4D2E8B6A1C'  # Static secret key for session management
socketio = SocketIO(app)

# Make session permanent and set it to a very long time (100 years)
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=365*100)

# Google Calendar API setup
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
creds = None

def get_google_creds():
    global creds
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)

        # Register a specific browser
        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser("/usr/bin/google-chrome"))  # Adjust this path as necessary
        webbrowser.get('chrome')  # Use the specified browser
        
        creds = flow.run_local_server(port=0)  # This will now try to open the specified browser
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def get_upcoming_events():
    service = build('calendar', 'v3', credentials=get_google_creds())
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    one_week_later = (datetime.datetime.utcnow() + datetime.timedelta(days=7)).isoformat() + 'Z'
    events_result = service.events().list(
        calendarId='primary',
        timeMin=now,
        timeMax=one_week_later,
        maxResults=50,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])
    return events

def categorize_events(events):
    events_by_day = defaultdict(list)
    colors = ['#ff7eb9', '#ff65a3', '#7afcff', '#feff9c', '#fff740']

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        start = datetime.datetime.fromisoformat(start)
        end = datetime.datetime.fromisoformat(end)

        # Use only the date part for categorization
        event_date = start.strftime('%Y-%m-%d')

        event_data = {
            'summary': event['summary'],
            'start': start,
            'end': end,
            'color': random.choice(colors),
            'duration_minutes': (end - start).total_seconds() / 60
        }

        events_by_day[event_date].append(event_data)

    return events_by_day

def convert_to_jalali(date):
    gregorian_date = datetime.datetime.combine(date, datetime.datetime.min.time())
    jalali_date = jdatetime.date.fromgregorian(date=gregorian_date)
    return jalali_date

def translate_day(day, language):
    days_english = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    days_persian = ['شنبه', 'یکشنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنج‌شنبه', 'جمعه']
    if language == 'persian':
        return days_persian[days_english.index(day)]
    return day




@app.route('/')
def index():
    language = request.args.get('lang', session.get('language', 'english'))
    dark_mode = request.args.get('dark_mode', 'off')  # Default is off
    session['language'] = language
    session.permanent = True  # Ensure the session is marked as permanent
    
    events = get_upcoming_events()
    events_by_day = categorize_events(events)

    days = []
    # Set the timezone for Iran
    iran_tz = pytz.timezone('Asia/Tehran')
    today = datetime.datetime.now(iran_tz)  # Get the current date and time in Iran timezone
    
    # Get the current time
    current_time = today.strftime('%H:%M')  # Format: HH:MM

    for i in range(7):
        current_day = today + datetime.timedelta(days=i)  # Increment by i days
        if language == 'persian':
            jalali_date = convert_to_jalali(current_day.date())
            day_obj = {
                'day_key': current_day.strftime('%Y-%m-%d'),
                'display_date': jalali_date.day,
                'day_name': translate_day(current_day.strftime('%A'), language)
            }
        else:
            day_obj = {
                'day_key': current_day.strftime('%Y-%m-%d'),
                'display_date': current_day.strftime('%d'),
                'day_name': translate_day(current_day.strftime('%A'), language)
            }
        days.append(day_obj)

    return render_template('index.html', events_by_day=events_by_day, days=days, language=language, dark_mode=dark_mode, current_time=current_time)



@app.route('/set_language/<language>')
def set_language(language):
    dark_mode = request.args.get('dark_mode', 'off')
    return redirect(url_for('index', lang=language, dark_mode=dark_mode))

@app.route('/set_dark_mode/<mode>')
def set_dark_mode(mode):
    language = request.args.get('lang', session.get('language', 'english'))
    return redirect(url_for('index', lang=language, dark_mode=mode))

@app.route('/reload')
def trigger_reload():
    socketio.emit('reload')
    return 'Reload triggered'

if __name__ == '__main__':
    socketio.run(app, debug=True)
