import os
import requests
from flask import Flask, redirect, request, render_template, session, url_for
from dotenv import load_dotenv
from markupsafe import escape

load_dotenv()

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World</p>"
#app.secret_key = ""

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'

with app.test_request_context():
    print(url_for('hello_world'))
    print(url_for('show_user_profile', username = "nfarrel2"))
    print(url_for('show_post', post_id=123))
    print(url_for('show_subpath', subpath='John/Doe'))