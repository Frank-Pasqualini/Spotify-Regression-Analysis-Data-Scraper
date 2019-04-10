import pickle

import math
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from pandas import DataFrame


def gather(data, category):
    """Organizes the data from the samples into an easy to use structure

        Keyword Arguments:
            data -- the data scraped from Spotify and Last.FM
            category -- the category of the data to organize
    """

    output = []
    # adj_variables are sets of category based on number of play counts. If a track has 5 plays and a tempo of 120 then
    # there are 5 values for tempo of 120 added the adj_tempo.  This is only useful for histograms
    if category[0:3] == "adj":
        for item in data:
            counter = 0
            while counter < int(item['playcount']):
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
    """Plots a histogram and saves it to the file

        Keyword Arguments:
            data -- the data in our variable structure
            title -- the category of the data to plot
    """

    # Can't plot strings in a histogram
    if title == 'name' or title == 'artist' or title == 'album':
        return

    plt.hist(x=data, bins='auto')
    plt.title(title + " (x̄=" + str(np.mean(data)) + " s=" + str(np.std(data)) + ")")
    plt.savefig("./Documentation/Graphs/Histograms/" + title + ".png")
    plt.close()


def plot_scatter(data, title, playcount):
    """Plots a scatter plot and saves it to the file

        Keyword Arguments:
            data -- the data in our variable structure
            title -- the category of the data to plot
            playcount -- the playcount data
    """

    # Can't plot strings in a scatter plot, no point in plotting adjusted sets or playcount vs playcount
    if title == 'name' or title == 'artist' or title == 'album' or title[0:3] == "adj" or title == 'playcount':
        return

    plt.plot(data, playcount, 'o')
    plt.title("playcount vs " + title)
    plt.savefig("./Documentation/Graphs/Scatter Plots/" + title + ".png")
    plt.close()


def transform(data):
    """Transforms the data to improve regression

        Keyword Arguments:
            data -- the data in our variable structure
    """

    transformed = {}

    for category in data:
        if category == "playcount" or category == "explicit" or category == "mode":
            transformed[category] = []
            for i, item in enumerate(data[category]):
                transformed[category].append(item)
        elif category != "name" and category != "artist" and category != "album" and category != "key" and category != "time_signature" and category[
                                                                                                                                            :3] != "adj":
            transformed[category] = []
            transformed[category + "_sq"] = []
            transformed[category + "_cu"] = []
            for i, item in enumerate(data[category]):
                transformed[category].append(item)
                transformed[category + "_sq"].append(item ** 2)
                transformed[category + "_cu"].append(item ** 3)

    temp = dict(transformed)

    for x in temp:
        for y in temp:
            if x != "playcount" and y != "playcount" and x[:3] > y[:3]:
                transformed[x + "X" + y] = []
                for i, item in enumerate(temp[x]):
                    transformed[x + "X" + y].append(temp[x][i] * temp[y][i])

    return transformed


def regress(data):
    """Makes a regression model with the data

        Keyword Arguments:
            data -- the data in our variable structure
    """

    df = DataFrame(data, columns=list(data))

    y = df['playcount']
    x = df.loc[:, df.columns != 'playcount']

    x = sm.add_constant(x)

    model = sm.OLS(y, x).fit()

    print_model = model.summary()
    print(print_model)


def mean_dif(data, category):
    if category == 'name' or category == 'artist' or category == 'album' or ("adj_" + category) not in data:
        return

    x1 = np.mean(data[category])
    x2 = np.mean(data["adj_" + category])
    s1 = np.std(data[category])
    s2 = np.std(data["adj_" + category])
    n1 = len(data[category])
    n2 = len(data["adj_" + category])

    t = (x1 - x2) / math.sqrt(((s1 ** 2) / n1) + ((s2 ** 2) / n2))

    print(category + " Difference of means vs adjusted t-score: " + str(t))


def main():
    # Reads data from the file
    out_file = open('output.data', 'rb')
    data = pickle.load(out_file)
    out_file.close()

    # A List of all of the variables we will be looking at
    category_lists = {'name': [], 'artist': [], 'album': [], 'playcount': [], 'duration_ms': [], 'adj_duration_ms': [],
                      'explicit': [], 'adj_explicit': [], 'popularity': [], 'adj_popularity': [], 'key': [],
                      'adj_key': [], 'mode': [], 'adj_mode': [], 'time_signature': [], 'adj_time_signature': [],
                      'acousticness': [], 'adj_acousticness': [], 'danceability': [], 'adj_danceability': [],
                      'energy': [], 'adj_energy': [], 'instrumentalness': [], 'adj_instrumentalness': [],
                      'liveness': [], 'adj_liveness': [], 'loudness': [], 'adj_loudness': [], 'speechiness': [],
                      'adj_speechiness': [], 'valence': [], 'adj_valence': [], 'tempo': [], 'adj_tempo': [],
                      'release_date': [], 'adj_release_date': [], 'album_popularity': [], 'adj_album_popularity': []}

    for category in category_lists:
        category_lists[category] = gather(data, category)
        plot_scatter(category_lists[category], category, category_lists['playcount'])
        plot_hist(category_lists[category], category)

    for category in category_lists:
        mean_dif(category_lists, category)

    # transformed = transform(category_lists)
    # regress(transformed)


if __name__ == "__main__":
    main()
