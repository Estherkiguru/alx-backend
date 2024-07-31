#!/usr/bin/env python3
""" Module for get_locale function"""
import pytz
from flask_babel import Babel, format_datetime
from flask import Flask, render_template, request, g
from datetime import datetime


class Config:
    """configuration class for configuration settings"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


"""Mock user database"""
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


app = Flask(__name__)
"""configure the Flask instance to use the config class"""
app.config.from_object(Config)
app.url_map.strict_slashes = False

"""Instantiate the Babel object"""
babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """Determines best language match with supported languages"""
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale

    if g.user and g.user['locale'] in app.config['LANGUAGES']:
        return g.user['locale']

    return request.accept_languages.best_match(app.config["LANGUAGES"])


@babel.timezoneselector
def get_timezone() -> str:
    """ Retrieves the timezone from request. """
    timezone = request.args.get('timezone', '').strip()
    if not timezone and g.user:
        timezone = g.user['timezone']
    try:
        return pytz.timezone(timezone).zone
    except pytz.exceptions.UnknownTimeZoneError:
        return app.config['BABEL_DEFAULT_TIMEZONE']


def get_user() -> dict:
    '''Returns a user dictionary based on URL parameter'''
    if request.args.get('login_as'):
        user = int(request.args.get('login_as'))
        if user in users:
            return users.get(user)
    else:
        return None


@app.before_request
def before_request():
    """Executes before each request to set the current user."""
    g.user = get_user()


@app.route('/')
def home_page() -> str:
    """ Route for the home page """
    timezone = get_timezone()
    tz = pytz.timezone(timezone)
    current_time = datetime.now(tz)
    current_time = format_datetime(datetime=current_time)
    return render_template("index.html", current_time=current_time)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
