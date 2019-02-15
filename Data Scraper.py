import spotipy.util
import spotipy
import random
import pylast
import credentials


def collect_data(sp):
    temp_results = sp.current_user_saved_tracks(50, 0)
    results = temp_results['items']
    counter = 1
    while len(temp_results['items']) == 51:
        temp_results = sp.current_user_saved_tracks(50, counter * 50)
        results = results + temp_results['items']
        counter = counter + 1
    return results


def get_attributes(sample, sp):
    attributes = []
    for item in sample:
        track_features = sp.audio_features(item['track']['id'])[0]
        playcount = 0  # TODO Actually collect playcount somehow
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

    spotify_scope = 'user-library-read'
    spotify_token = spotipy.util.prompt_for_user_token(credentials.spotify_username, spotify_scope,
                                                       client_id=credentials.spotify_api_key,
                                                       client_secret=credentials.spotify_api_secret,
                                                       redirect_uri=credentials.spotify_redirect_uri)

    lastfm_network = pylast.LastFMNetwork(api_key=credentials.lastfm_api_key,
                                          api_secret=credentials.lastfm_api_secret,
                                          username=credentials.lastfm_username,
                                          password_hash=credentials.lastfm_password_hash)

    if spotify_token and lastfm_network:
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
