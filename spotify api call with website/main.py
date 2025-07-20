from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

app = Flask(__name__)

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    params = {
        "q": artist_name,
        "type": "artist",
        "limit": 1
    }
    result = get(url, headers=headers, params=params)
    json_result = json.loads(result.content)["artists"]["items"]
    if not json_result:
        return None
    return json_result[0]

def artist_songs(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result[:10]  # Limit to top 10 songs

@app.route("/", methods=["GET", "POST"])
def index():
    songs = []
    artist_name = ""
    error = None
    if request.method == "POST":
        artist_name = request.form.get("artist_name")
        token = get_token()
        artist = search_artist(token, artist_name)
        if artist:
            songs = artist_songs(token, artist["id"])
        else:
            error = "Artist not found."
    return render_template("index.html", songs=songs, artist_name=artist_name, error=error)

if __name__ == "__main__":
    app.run(debug=True)