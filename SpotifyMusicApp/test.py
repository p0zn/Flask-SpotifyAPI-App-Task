from flask import Flask, render_template, request,url_for,jsonify
import json
import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


app = Flask(__name__, template_folder="templates")
app.secret_key = "verysecretkey"


client_id = "bca7d0f35f3d4a7f92485baa641da984"
client_secret = "ad7df78ae3e04475828c5dabeaa9a4eb"
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) 

with open("genres.json","r") as file: 
   data = json.load(file)

genres = list(data.keys())
artists = list(data.values())

@app.route("/")
def index():

   m_type = request.args.get("type") 
   if m_type in genres:
      m_index = genres.index(m_type)
      if m_type == genres[m_index]:
         a = random.choice(artists[m_index])
         name = {a}
         result = sp.search(name)
         artist_uri = result['tracks']['items'][0]['artists'][0]['uri']
         top_music = sp.artist_top_tracks(artist_uri)
         top_music_list = []
         for track in top_music['tracks'][:10]:
            top_music_list.append([
            'name     : ' + str(list(name)),      
            'track    : ' + track['name'], 
            'album_image_url: ' + track['album']['images'][0]['url'],
              ])
      return jsonify(top_music_list)
   return render_template("index.html", m_type = m_type)


if __name__ == "__main__":
    app.run(debug=True)

