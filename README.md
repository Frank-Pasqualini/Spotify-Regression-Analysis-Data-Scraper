# Spotify Regression Analysis Data Scraper

This is a project I am working on for my Applied Regression Writing class.  The goal of this tool is to pull in my entire Spotify library to try to build and analyze a multiple regression model with my playcount (retrieved from Last.fm) as the response variable and features of the track, such as tempo, duration, energy, etc. as the predictor variables.  I decided to choose this project because it combines my 3 biggest passions, Computer Science, Data Analysis, and Music. 

### Prerequisites

This project requires both the Spotipy and pyLast libraries, which can be installed as follows:

```
pip install spotipy pylast
```

## Getting Started

To run this script, all you need to do is clone to your machine and create a file named credentials.py, which contains the following:

```python
import pylast

spotify_username = "YOUR USERNAME"
spotify_api_key = "726bfaf7c99a484d95e38ba78c69b315"
spotify_api_secret = "REDACTED" # TODO I am still trying to make this work while remaining secure
spotify_redirect_uri = "http://localhost:8888/"

lastfm_username = "YOUR USERNAME"
lastfm_api_key = "f8fa93dcc38cf66cfde99abf180ddaf8"
lastfm_api_secret = "REDACTED" # TODO I am still trying to make this work while remaining secure
lastfm_password_hash = pylast.md5("YOUR PASSWORD")

```

You can then run the script with:
```bash
python "Data Scraper.py"
```

## Built With

* [Spotipy](https://github.com/plamere/spotipy) - A framework to use Spotify's web API in python
* [pyLast](https://github.com/pylast/pylast) - a framework to use Last.fm's web API in python

## Authors

* **Frank Pasqualini**