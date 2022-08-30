from flask import Flask, render_template, request,url_for,session,redirect
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth 
import time  

app = Flask(__name__, template_folder="templates")
app.secret_key = "verysecretkey"
app.config["SESSION_COOKIE_NAME"] = "Spotify App"
TOKEN_INFO = "token_info"

with open("genres.json","r") as file: 
   data = json.load(file)

genres = data.keys()
artists = data.values()

genres_list = []
artist_list = []

for genre in genres:
    genres_list.append(genre)

for artist in artists:
    for i in artist:
        artist_list.append(i)
print(artist_list)


#     if genre in genres:
#         print(data.values())
#     return render_template("index.html",genre=genre)

@app.route("/")
def login():
   sp_oauth = create_spotify_oauth()
   auth_url = sp_oauth.get_authorize_url()
   return redirect(auth_url)


@app.route("/redirect")
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get("code")
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('getTracks',_external = True))


@app.route("/getTracks")
def getTracks():
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        return redirect(url_for("login",_external=False))
    sp = spotipy.Spotify(auth=token_info['access_token'])
    return sp.current_user_saved_tracks(limit=50)

def get_token():
    token_info = session.get(TOKEN_INFO,None)
    if not token_info:
        raise "exception"
    now = int(time.time())

    is_expired = token_info["expires_at"] - now < 60 
    if is_expired:
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])
    return token_info

@app.route("/tracks/<genre>")
def display():
    return render_template("display.html")


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id = "bca7d0f35f3d4a7f92485baa641da984",
        client_secret = "ad7df78ae3e04475828c5dabeaa9a4eb",
        redirect_uri=url_for('redirectPage',_external = True),
        scope = "user-library-read"
    )
























if __name__ == "__main__":
    app.run(debug=True)