import pickle

import matplotlib.pyplot as plt
import numpy as np


def gather(data, category):
    output = []
    if category[0:3] == "adj":
        for item in data:
            counter = 0
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
    plt.savefig("./Documentation/Graphs/Histograms/" + title + ".png")
    plt.close()


def plot_scatter(data, title, playcount):
    if title == 'name' or title == 'artist' or title == 'album' or title[0:3] == "adj" or title == 'playcount':
        return

    plt.plot(data, playcount, 'o')
    plt.title("playcount vs " + title)
    plt.savefig("./Documentation/Graphs/Scatter Plots/" + title + ".png")
    plt.close()


def main():
    # Reads data from the file
    out_file = open('output.data', 'rb')
    data = pickle.load(out_file)
    out_file.close()

    category_lists = {'name': [], 'artist': [], 'album': [], 'playcount': [], 'duration_ms': [], 'adj_duration_ms': [],
                      'explicit': [], 'adj_explicit': [], 'popularity': [], 'adj_popularity': [], 'key': [],
                      'adj_key': [], 'mode': [], 'adj_mode': [], 'time_signature': [], 'adj_time_signature': [],
                      'acousticness': [], 'adj_acousticness': [], 'danceability': [], 'adj_danceability': [],
                      'energy': [], 'adj_energy': [], 'instrumentalness': [], 'adj_instrumentalness': [],
                      'liveness': [], 'adj_liveness': [], 'loudness': [], 'adj_loudness': [], 'speechiness': [],
                      'adj_speechiness': [], 'valence': [], 'adj_valence': [], 'tempo': [], 'adj_tempo': []}

    for category in category_lists:
        category_lists[category] = gather(data, category)
        plot_scatter(category_lists[category], category, category_lists['playcount'])
        plot_hist(category_lists[category], category)


if __name__ == "__main__":
    main()
