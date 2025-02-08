#!/usr/bin/python3
"""
Flask web application that listens on 0.0.0.0, port 5000,
Displays "Hello HBNB!" when accessing the root URL
"""

from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_route():
    """Returns a greeting message"""
    return "Hello HBNB!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
