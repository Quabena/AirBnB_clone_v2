#!/usr/bin/python3
"""
Flask web application that listens on 0.0.0.0, port 5000,
Displays "Hello HBNB!" on the root URL.
Displays "HBNB" on the /hbnb route
"""

from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_route():
    """Returns a greeting message for the root route"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Returns 'HBNB' for the /hbnb route"""
    return "HBNB"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
