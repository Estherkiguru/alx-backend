#!/usr/bin/env python3
""" Module for setting up a basic Flask app """
from flask import Flask, render_template

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/")
def welcome_page():
    """ Route for the welcome page """
    return render_template('0-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
