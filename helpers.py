# helpers.py
import datetime
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import requests

def fetch_listening_data(access_token, limit=15):
    headers = {'Authorization': f'Bearer {access_token}'}
    tracks = []
    offset = 0

    while offset < limit:
        response = requests.get('https://api.spotify.com/v1/me/player/recently-played', headers=headers, params={'limit': min(50, limit - offset), 'offset': offset})

        if response.status_code == 200:
            data = response.json()
            new_tracks = data.get('items', [])
            if not new_tracks:
                break

            tracks.extend(new_tracks)
            offset += len(new_tracks)

        else:
            print(f"Failed to fetch listening data. Status code: {response.status_code}")
            break

    if len(tracks) > 0:
        return tracks[:limit]  # Return only the first 500 tracks if there are more than 500
    else:
        print("No listening data available.")
        return None



def process_listening_data(listening_data):
    # Initialize dictionaries to store listening times and days of the week
    listening_times = {}
    listening_days = {day: 0 for day in range(7)}  # Initialize each day with 0 plays

    for track in listening_data:
        # Extract the timestamp when the track was played
        timestamp = track['played_at']

        # Convert the timestamp to a datetime object
        play_time = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')

        # Extract the hour of the day when the track was played
        hour = play_time.hour

        # Increment the play count for the specific hour in the listening_times dictionary
        if hour in listening_times:
            listening_times[hour] += 1
        else:
            listening_times[hour] = 1

        # Extract the day of the week when the track was played (0 = Monday, 6 = Sunday)
        day_of_week = play_time.weekday()

        # Increment the play count for the specific day of the week in the listening_days dictionary
        listening_days[day_of_week] += 1

    return listening_times, listening_days
# helpers.py


def extract_artist_track_name(track_data):
    artist_name = track_data.get('artists', [{}])[0].get('name', '')
    track_name = track_data.get('name', '')
    return f"{artist_name} - {track_name}"