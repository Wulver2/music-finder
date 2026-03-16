from flask import Flask, render_template, request
#from dotenv import load_dotenv
import requests
import os

app = Flask(__name__)
# TODO: Format data, implement recommendation system, try autocomplete system,
# add a way to go back to homepage after artist post

#load_dotenv()
email = os.getenv("MB_EMAIL")

headers = {
    'User-Agent': f'MusicFinder/0.0.1 ({email})'
    #"Accept" : "application/json"
}
api_url = "https://musicbrainz.org/ws/2/"

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/', methods=["POST"])
def info():
    artist_name = request.form.get("userArtist")
    print(artist_name)
    info = get_artists_info(artist_name)
    tags = info["artists"][0]["tags"]

    return render_template("artists.html", info= tags)

# TODO: Will allow retrival of other artists that match initial artist entered
# 
def make_recommendation(artist_info):
    pass

def get_artists_info(artist):


    #url = f"{api_url}?query=artist:{artist}?inc=aliases&fmt=json"
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