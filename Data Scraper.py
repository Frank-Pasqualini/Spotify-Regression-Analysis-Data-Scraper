import random

import requests
import spotipy
import spotipy.util

import config  # TODO Better way to store credentials


def collect_data(sp):
    """Collects all of the tracks from a user's Spotify library

    Keyword Arguments:
        sp -- The Spotify authorized session
    """
    temp_results = sp.current_user_saved_tracks(50, 0)  # Collects the first 50 songs in the user's library
    results = temp_results['items']

    counter = 50
    while len(temp_results['items']) == 50:  # Keeps running until less than 50 items are returned, which is the end
        temp_results = sp.current_user_saved_tracks(50, counter)
        results = results + temp_results['items']
        counter = counter + 50

    return results


def get_attributes(sample, sp, lastfm_api_key, lastfm_username):
    """Gets all of the attributes of tracks from a sample

        Keyword Arguments:
            sample -- The list of tracks
            sp -- The Spotify authorized session
            lastfm_api_key -- The API Key for Last.fm requests
            lastfm_username -- The username for Last.fm requests
    """
    attributes = []
    for item in sample:
        # Some attributes are stored in the track and some can only be retrieved from track_features
        track_features = sp.audio_features(item['track']['id'])[0]
        # Gets the data stored by Last.fm, including the user's playcount
        r = requests.get(url="http://ws.audioscrobbler.com/2.0/?method=track.getInfo",
                         params={'api_key': lastfm_api_key,
                                 'track': item['track']['name'],
                                 'artist': item['track']['artists'][0]['name'],
                                 'username': lastfm_username,
                                 'format': "json"})

        try:
            try:
                data = r.json()
                track = data['track']
            except KeyError:
                print("Error track not returned properly")
                continue
            playcount = track['userplaycount']
        except KeyError:  # If  there is no playcount value it means that last.fm did not collect the data correctly
            print("Playcount not found for " + r.json()['track']['name'] + " - " + r.json()['track']['artist']['name'])
            playcount = 1  # I have listened to every song in my Spotify library at least once
            # There could be issues detecting due to listening on other platforms that have not been linked to Last.fm,
            # such as live performances, the radio, or streaming platforms like Youtube.

        track = [{'name': item['track']['name'],
                  'artist': item['track']['artists'][0]['name'],
                  'album': item['track']["album"]["name"],
                  'playcount': playcount,
                  'duration_ms': item['track']['duration_ms'],
                  'explicit': item['track']['explicit'],
                  'popularity': item['track']['popularity'],
                  'key': track_features['key'],
                  'mode': track_features['mode'],
                  'time_signature': track_features['time_signature'],
                  'acousticness': track_features['acousticness'],
                  'danceability': track_features['danceability'],
                  'energy': track_features['energy'],
                  'instrumentalness': track_features['instrumentalness'],
                  'liveness': track_features['liveness'],
                  'loudness': track_features['loudness'],
                  'speechiness': track_features['speechiness'],
                  'valence': track_features['valence'],
                  'tempo': track_features['tempo']}]
        attributes = attributes + track
    return attributes


def main():
    spotify_api_key = "726bfaf7c99a484d95e38ba78c69b315"
    spotify_redirect_uri = "http://localhost:8888/"
    spotify_scope = 'user-library-read'  # Gives permission to read the user's spotify library

    lastfm_api_key = "f8fa93dcc38cf66cfde99abf180ddaf8"

    # Authorizes the user so Spotify's API can access their data.  Potential TODO streamline the process
    spotify_token = spotipy.util.prompt_for_user_token(config.spotify_username, spotify_scope,
                                                       client_id=spotify_api_key,
                                                       client_secret=config.spotify_api_secret,
                                                       redirect_uri=spotify_redirect_uri)

    if spotify_token:
        sp = spotipy.Spotify(auth=spotify_token)

        dataset = collect_data(sp)

        if config.sample_size > len(dataset):
            sample = dataset
        else:
            sample = random.sample(dataset, config.sample_size)

        attributes = get_attributes(sample, sp, lastfm_api_key, config.lastfm_username)

        for item in attributes:
            print(item)  # TODO Analyze Data
    else:
        print("Can't get Spotify token for ", config.spotify_username)


if __name__ == "__main__":
    main()
