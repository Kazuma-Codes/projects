from dotenv import load_dotenv
import os
import base64
from requests import post,get
import json 

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes),"utf-8")

    url = "https://accounts.spotify.com/api/token"

    headers = {
        "Authorization" : "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type" : "client_credentials"}
    result = post(url,headers = headers,data = data) # post 
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
        "type": "artist,album",
        "limit": 2
    }

    result = get(url, headers=headers, params=params)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("not found")
        return None
    return json_result[0]

def artist_songs(token, id):
    url = f"https://api.spotify.com/v1/artists/{id}/top-tracks"
    headers = get_auth_header(token)
    result = get(url,headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

token = get_token() 
result = search_artist(token,"sabrina carpenter" )
#print(result["name"])
id = result["id"]
songs = artist_songs(token,id)
for index , song in enumerate(songs):
    print(f"{index + 1}. {song['name']}")