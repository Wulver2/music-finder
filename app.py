from flask import Flask, render_template, request
import pandas as pd
import requests
import os

app = Flask(__name__)
# TODO: Format data, implement recommendation system, try autocomplete system,
# add a way to go back to homepage after artist post

email = os.getenv("MB_EMAIL")

headers = {
    'User-Agent': f'MusicFinder/0.0.1 ({email})'
}

# Chose to use the url instead of the musicbrainz library in order to
# have more practice with APIs in this form
api_url = "https://musicbrainz.org/ws/2/"

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/', methods=["POST"])
def info():
    artist_name = request.form.get("userArtist")
    info = get_artists_info(artist_name)
    tags = info["artists"][0]["tags"]

    return render_template("artists.html", info=make_recommendation(tags), name=artist_name)

# Artists with similar genres to the initial artists will be returned and later
# formatted to new page
def make_recommendation(artist_info):
    # Instead of going through each tag that an artists has may only use the one with
    # the highest count? artists with too many tags slow down size since they make multiple
    # requests
    new_artists = set()

    for tag in range(len(artist_info)):
        genre = artist_info[tag]["name"]
        new_artists_url = f"https://musicbrainz.org/ws/2/artist/?query=tag:\"{genre}\"&fmt=json"
        response = requests.get(new_artists_url, headers=headers)
        data = response.json()

        for artist_index in range(len(data["artists"])):
            artist = data["artists"][artist_index]["name"]
            if artist not in new_artists:
                new_artists.add(artist)

    return new_artists

# Returned json file will be used to extract tags and any other data that 
# will be useful for making artist recommendations
def get_artists_info(artist):

    url = f"{api_url}artist/?query=artist:{artist}&fmt=json"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print(f"data retrieved")
        return data
    elif response.status_code == 403:
        print("need a user-agent")
    else:
        print("error")

# artist_name = "Vince_Staples"
# get_artists_info(artist_name)


if __name__ == '__main__n':
    app.run(debug="True")