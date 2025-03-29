import os
import requests
from flask import Flask, redirect, request, render_template, session, url_for
from dotenv import load_dotenv
from markupsafe import escape
from flask_bootstrap import Bootstrap

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET")

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
    auth_url = f"{AUTH_URL}?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPE}"
    return redirect(auth_url)
    
@app.route("/callback")
def callback():
    code = request.args.get("code")
    token_data = {
        "grant_type" : "authorization_code",
        "code" : code,
        "redirect_uri" : REDIRECT_URI,
        "client_id" : CLIENT_ID,
        "client_secret" : CLIENT_SECRET
    }








'''
@app.route("/login")
def login():
    auth_url = f"{AUTH_URL}?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPE}"
    return redirect(auth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    response = requests.post(TOKEN_URL, data=token_data).json()

    # Store access token in session
    session["access_token"] = response.get("access_token")

    return redirect(url_for("dashboard"))

@app.route("/dashboard")
def dashboard():
    if "access_token" not in session:
        return redirect(url_for("home"))

    headers = {"Authorization": f"Bearer {session['access_token']}"}
    
    # Fetch recently played tracks
    recent_tracks = requests.get(API_BASE_URL + "me/player/recently-played", headers=headers).json()
    
    # Fetch user playlists
    playlists = requests.get(API_BASE_URL + "me/playlists", headers=headers).json()

    return render_template("dashboard.html", recent_tracks=recent_tracks.get("items", []), playlists=playlists.get("items", []))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)'''