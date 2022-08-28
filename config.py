"""Flask config."""
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Flask configuration variables."""

    # General Config
    SECRET_KEY = "UYi7KVumXTIBxd3"
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')
    GOOGLE_OAUTH_CLIENT_ID="CLIENT_ID"
    GOOGLE_OAUTH_CLIENT_SECRET="CLIENT_SECRET"
    environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    # Assets
    LESS_BIN = environ.get('LESS_BIN')
    ASSETS_DEBUG = environ.get('ASSETS_DEBUG')
    LESS_RUN_IN_DEBUG = environ.get('LESS_RUN_IN_DEBUG')

    # Static Assets
    STATIC_FOLDER = environ.get('STATIC_FOLDER')
    TEMPLATES_FOLDER = environ.get('TEMPLATES_FOLDER')
    COMPRESSOR_DEBUG = environ.get('COMPRESSOR_DEBUG')
