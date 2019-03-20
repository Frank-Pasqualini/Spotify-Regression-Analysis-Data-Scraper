import pickle

import matplotlib.pyplot as plt
import numpy as np


def gather(data, category):
    output = []
    if category[0:3] == "adj":
        counter = 0
        for item in data:
            while counter < int(item['playcount']):
                if category == 'name' or category == 'artist' or category == 'album':
                    output.append(item[category[4:]])
                else:
                    output.append(float(item[category[4:]]))
                counter = counter + 1
    else:
        for item in data:
            if category == 'name' or category == 'artist' or category == 'album':
                output.append(item[category])
            else:
                output.append(float(item[category]))
    return output


def plot_hist(data, title):
    if title == 'name' or title == 'artist' or title == 'album':
        return

    plt.hist(x=data, bins='auto')
    plt.title(title + " (x̄=" + str(np.mean(data)) + " s=" + str(np.std(data)) + ")")
    plt.show()


def plot_scatter(data, title, playcount):
    if title == 'name' or title == 'artist' or title == 'album' or title[0:3] == "adj":
        return

    plt.plot(data, playcount, 'o')
    plt.title("playcount vs " + title)
    plt.show()


def main():
    # Reads data from the file
    out_file = open('output.data', 'rb')
    data = pickle.load(out_file)
    out_file.close()

    category_lists = {'name': [], 'artist': [], 'album': [], 'playcount': [], 'duration_ms': [], 'explicit': [],
                      'popularity': [], 'key': [], 'mode': [], 'time_signature': [], 'acousticness': [],
                      'danceability': [], 'energy': [], 'instrumentalness': [], 'liveness': [], 'loudness': [],
                      'speechiness': [], 'valence': [], 'tempo': [], 'adj_duration_ms': [], 'adj_explicit': [],
                      'adj_popularity': [], 'adj_key': [], 'adj_mode': [], 'adj_time_signature': [],
                      'adj_acousticness': [], 'adj_danceability': [], 'adj_energy': [], 'adj_instrumentalness': [],
                      'adj_liveness': [], 'adj_loudness': [], 'adj_speechiness': [], 'adj_valence': [], 'adj_tempo': []}

    for category in category_lists:
        category_lists[category] = gather(data, category)
        plot_hist(category_lists[category], category)
        plot_scatter(category_lists[category], category, category_lists['playcount'])


if __name__ == "__main__":
    main()
