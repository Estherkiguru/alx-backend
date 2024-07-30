#!/usr/bin/env python3
""" Module for get_locale function"""
from flask_babel import Babel
from flask import Flask, render_template, request, g


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
    return request.accept_languages.best_match(app.config["LANGUAGES"])


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
    return render_template('5-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
