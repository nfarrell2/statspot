import os, requests, urllib.parse
from flask import Flask, redirect, request, render_template, session, url_for
from dotenv import load_dotenv
from markupsafe import escape
from flask_bootstrap import Bootstrap
from datetime import timedelta

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET")

app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=1)


CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE_URL = "https://api.spotify.com/v1/"
SCOPE = "playlist-read-private playlist-modify-private user-top-read user-read-recently-played user-library-read"

@app.route("/")
def home():
    return render_template("index.html", logged_in = "access_token" in session)

@app.route("/login")
def login():
    scope_encoded = urllib.parse.quote(SCOPE)
    auth_url = f"{AUTH_URL}?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={scope_encoded}"
    return redirect(auth_url)
    
@app.route("/callback")
def callback():
    code = request.args.get("code")

    token_data = {
        "grant_type" : "authorization_code",
        "code" : code,
        "redirect_uri" : REDIRECT_URI,
        "client_id" : CLIENT_ID,
        "client_secret" : CLIENT_SECRET,
    }

    response = requests.post(TOKEN_URL, data=token_data).json()

    session.permanent = True
    session["access_token"] = response.get("access_token")
    session["refresh_token"] = response.get("refresh_token")
    session["expires_in"] = response.get("expires_in")

    return redirect(url_for("dashboard"))

@app.route("/dashboard")
def dashboard():
    if "access_token" not in session:
        return redirect(url_for("home"))
    
    headers = {"Authorization" : f"Bearer {session['access_token']}"}

    top_artists = requests.get(API_BASE_URL + "me/top/artists?limit=10", headers=headers).json()["items"]

    top_tracks = requests.get(API_BASE_URL + "me/top/tracks?limit=10", headers=headers).json()["items"]

    top_genres = dict()

    total_pop = 0

    for i in range(len(top_artists)):
        artist = top_artists[i]
        for genre in artist["genres"]:
            if genre in top_genres:
                top_genres[genre] += 1
            else:
                top_genres[genre] = 1
        total_pop += artist["popularity"]
        top_artists[i] = top_artists[i]["name"]
    
    for i in range(len(top_tracks)):
        track = top_tracks[i]
        total_pop += track["popularity"]
        top_tracks[i] = {k: v for k, v in top_tracks[i].items() if k in {"name", "artists"}}
        for j in range(len(top_tracks[i]["artists"])):
            top_tracks[i]["artists"][j] = top_tracks[i]["artists"][j]["name"]

    avg_pop = (float) (total_pop / 20.0)

    return render_template("dashboard.html", top_Artists=top_artists, top_Songs=top_tracks, top_Genres=top_genres, avg_Popularity=avg_pop)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
