"""Core Flask app routes."""
from flask import render_template, redirect, url_for
from flask import current_app as app

from authlib.client import OAuth2Session
import google.oauth2.credentials
import googleapiclient.discovery
from dash_google_auth import google_auth

app.register_blueprint(google_auth.app)

@app.route('/')
def home():
    """Landing page."""
    if google_auth.is_logged_in():
        return render_template(
            'index.jinja2',
            title='Dashboard',
            description='Dashboard',
            template='home-template',
            body="This is a homepage.",
            user_info=google_auth.get_user_info()
        )
    
    return redirect(url_for("google_auth.login"))
