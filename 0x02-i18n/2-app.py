#!/usr/bin/env python3
""" Module for get_locale function"""
from flask_babel import Babel
from flask import Flask, render_template, request


class Config:
    """configuration class for configuration settings"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
"""configure the Flask instance to use the config class"""
app.config.from_object(Config)
app.url_map.strict_slashes = False

"""Instantiate the Babel object"""
babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """Determines best match with supported languages"""
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route('/')
def home_page() -> str:
    """ Route for the home page """
    return render_template('2-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
