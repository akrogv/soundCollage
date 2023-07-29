from flask import Flask, render_template, redirect, url_for, session, request
from flask_oauthlib.client import OAuth
from helpers import *
import requests
import json
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
SPOTIFY_SCOPES = ['user-read-recently-played user-read-private user-library-read user-read-email playlist-read-private user-top-read']

oauth = OAuth(app)

spotify = oauth.remote_app(
    'spotify',
    request_token_params={
        'scope':SPOTIFY_SCOPES,},
    base_url='https://api.spotify.com/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.spotify.com/api/token',
    authorize_url='https://accounts.spotify.com/authorize',
    consumer_key='96626927888642e5bedd41bf75518c59',  # Your client_id goes here
)

@app.route('/')
def home():
    # Check if the user is logged in (i.e., has an access token)
    access_token = session.get('spotify_token')

    # Redirect to the profile page if the user is logged in
    if access_token:
        return redirect(url_for('profile'))

    # If the user is not logged in, show the login page
    return render_template('index.html', user_data='')


@app.route('/login')
def login():
    return spotify.authorize(callback=url_for('spotify_authorized', _external=True))


@app.route('/spotify_authorized')
def spotify_authorized():
    response = spotify.authorized_response()
    if response is None or response.get('access_token') is None:
        # Handle authentication failure
        return redirect(url_for('login'))

    # Save the access token and refresh token in the session
    session['spotify_token'] = response['access_token']
    session['spotify_refresh_token'] = response.get('refresh_token')

    # Redirect to the home page or any other route
    return redirect(url_for('collage'))

@app.route('/profile')
def profile():
    access_token = session.get('spotify_token')
    if not access_token:
        return redirect(url_for('login'))
        # Fetch the user's profile data from the Spotify API
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('https://api.spotify.com/v1/me', headers=headers)
    # Check if the API request was successful
    if response.status_code == 200:
        user_data = response.json()
        # Extract the relevant user data (e.g., display name, email, profile picture, etc.)
        display_name = user_data.get('display_name', 'User')
        email = user_data.get('email', '')
        profile_picture = None
        images = user_data.get('images',[])
        if images:
            profile_picture = images[0].get('url')
        #fetch listening data
        timerange = request.args.get('time_range','short_term')
        top_tracks_url = 'https://api.spotify.com/v1/me/top/tracks'
        response = requests.get(top_tracks_url,headers=headers,params={'limit':3,'time_range':'short_term'})
        print(response)
        if response.ok and response.text:
            try:
                top_tracks_data = response.json()
                top_tracks = top_tracks_data['items']
        # Render the 'profile.html' template with the user data
                return render_template('profile.html', display_name=display_name,top_tracks=top_tracks ,email=email)#,profile_picture=profile_picture
            except json.JSONDecoder as e:
                print(f"JSONDecodeeRROR: {e}")
        else:
            print(f"failed to fetch data.{response.status_code}")
    # If the API request fails or the access token is invalid, redirect to the login page
    return redirect(url_for('login'))


@app.route('/collage')
def collage():
    access_token = session.get('spotify_token')
    if not access_token:
        return redirect(url_for('login'))

    # Fetch the user's top tracks data from the Spotify API
    limit= 50
    headers = {'Authorization': f'Bearer {access_token}'}
    top_tracks_url = 'https://api.spotify.com/v1/me/top/tracks'
    timerange=request.args.get('time_range','short_term')
    response = requests.get(top_tracks_url, headers=headers, params={'limit':{limit},'time_range':{timerange}})

    if response.status_code == 200:
        top_tracks_data = response.json()
        top_tracks = top_tracks_data.get('items')

        # Extract album images from the top tracks
        album_images_set = set()
        for track in top_tracks:
            album_images_set.add(track['album']['images'][0]['url'])
            if len(album_images_set)>= 25:
                break
        album_images = list(album_images_set)

        # Render the 'collage.html' template with the album_images data
        return render_template('collage.html', album_images=album_images)

    else:
        print(f"Failed to fetch top tracks data. Status code: {response.status_code}")
        print(response.text)  # Print the response data for debugging purposes
        return render_template('error.html', message='Failed to fetch top tracks data')


@app.route('/logout')
def logout():
    # Clear the session data, including access token and refresh token
    session.pop('spotify_token', None)
    session.pop('spotify_refresh_token', None)
    session.clear()

    # Redirect the user to the home page (or any other desired page)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.debug = True
    app.run()
