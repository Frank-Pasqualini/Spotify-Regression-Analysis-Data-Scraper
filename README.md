# Spotify Regression Analysis Data Scraper

This is a project I am working on for my Applied Regression Writing class.  The goal of this tool is to pull in my entire Spotify library to try to build and analyze a multiple regression model with my playcount (retrieved from Last.fm) as the response variable and features of the track, such as tempo, duration, energy, etc. as the predictor variables.  I decided to choose this project because it combines my 3 biggest passions, Computer Science, Data Analysis, and Music. 

### Prerequisites

This project requires both the Spotipy and requests libraries, which can be installed as follows:

```
pip install spotipy requests
```

## Getting Started

To run this script, all you need to do is clone to your machine and create a file named config.py, which contains the following:

```python
spotify_username = "YOUR USERNAME"
spotify_api_secret = "REDACTED"  # TODO I am still trying to make this work while remaining secure

lastfm_username = "YOUR USERNAME"

sample_size = 30

```

You can then run the script to collect the data with:
```bash
python "Data Scraper.py"
```

and run the script to analyze the data with:
```bash
python "Data Analysis.py"
```

## Built With

* [Spotipy](https://github.com/plamere/spotipy) - A framework to use Spotify's web API in python
## Authors

* **Frank Pasqualini**