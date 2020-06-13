"""Initialize Flask app."""
from flask import Flask
from flask_assets import Environment

#from authlib.client import OAuth2Session
#import google.oauth2.credentials
#import googleapiclient.discovery
#import google_auth

def create_app():
    """Construct core Flask application with embedded Dash app."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    #app.register_blueprint(google_auth.app)
    assets = Environment()
    assets.init_app(app)
    
    #if google_auth.is_logged_in():
    with app.app_context():
        # Import parts of our core Flask app
        from . import routes
        from .assets import compile_static_assets

        # Import Dash application
        from .plotlydash.dashboard import create_dashboard
        app = create_dashboard(app)

        # Compile static assets
        compile_static_assets(assets)

        return app
