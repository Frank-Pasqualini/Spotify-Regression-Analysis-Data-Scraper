import spotipy.util
import spotipy
import random
import pylast
import credentials  # TODO Better way to store credentials


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


def get_attributes(sample, sp):
    """Gets all of the attributes of tracks from a sample

        Keyword Arguments:
            sample -- The list of tracks
            sp -- The Spotify authorized session
    """
    attributes = []
    for item in sample:
        # Some attributes are stored in the track and some can only be retrieved from track_features
        track_features = sp.audio_features(item['track']['id'])[0]
        playcount = 0  # TODO Actually collect playcount somehow, probably with pylast

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
    sample_size = 30  # TODO modifiable sample size

    spotify_scope = 'user-library-read'  # Gives permission to read the user's spotify library

    # Authorizes the user so Spotify's API can access their data.  Potential TODO streamline the process
    spotify_token = spotipy.util.prompt_for_user_token(credentials.spotify_username, spotify_scope,
                                                       client_id=credentials.spotify_api_key,
                                                       client_secret=credentials.spotify_api_secret,
                                                       redirect_uri=credentials.spotify_redirect_uri)

    # Authorizes the API to access the user's Last.fm profile
    lastfm_network = pylast.LastFMNetwork(api_key=credentials.lastfm_api_key,
                                          api_secret=credentials.lastfm_api_secret,
                                          username=credentials.lastfm_username,
                                          password_hash=credentials.lastfm_password_hash)

    if spotify_token and lastfm_network:
        print("Retrieved Spotify token and Last.fm network")
        sp = spotipy.Spotify(auth=spotify_token)

        dataset = collect_data(sp)
        sample = random.sample(dataset, sample_size)
        attributes = get_attributes(sample, sp)

        for item in attributes:
            print(item)  # TODO Analyze Data
    elif not spotify_token:
        print("Can't get Spotify token for ", credentials.spotify_username)
    else:
        print("Can't get Last.fm network for ", credentials.lastfm_username)


if __name__ == "__main__":
    main()
