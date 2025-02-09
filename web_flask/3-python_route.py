#!/usr/bin/python3
"""
Flask web application that starts a server with multiple routes.
"""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Returns 'Hello HBNB!' on the root route"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Returns 'HBNB' on the /hbnb route"""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_route(text):
    """
    Returns 'C ' followed by the text variable with
    underscores replaced by spaces
    """
    return "C {}".format(text.replace('_', ' '))


@app.route("/python", defaults={'text': 'is cool'}, strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python_route(text):
    """
    Returns 'Python ' followed by the text variable
    with underscores replaced by spaces
    """
    return "Python {}".format(text.replace('_', ' '))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
