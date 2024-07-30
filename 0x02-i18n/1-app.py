#!/usr/bin/env python3
""" Module for instantiating Babel object in app """
from flask import Flask, render_template
from flask_babel import Babel


class Config:
    """configuration class for configuration settings"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULE_TIMEZONE = "UTC"


app = Flask(__name__)
"""configure the Flask instance to use the config class"""
app.config.from_object(Config)
app.url_map.strict_slashes = False

"""Instantiate the Babel object"""
babel = Babel(app)


@app.route("/")
def welcome_page() -> str:
    """ Route for the welcome page """
    return render_template('1-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
