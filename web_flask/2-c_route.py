#!/usr/bin/python3
"""
Flask web application that listens on 0.0.0.0, port 5000,
Displays "Hello HBNB!" on the root route
Displays "HBNB" on the /hbnb route
Displays "C <text>" on the /c/<text> route, replacing uderscores with spaces
"""

from flask import Flask

app = Flask("__name__")


@app.route("/", strict_slashes=False)
def hello_route():
    """Returns a greeting message for the root route"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slahes=False)
def hbnb():
    """Returns 'HBNB' for the /hbnb route"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_text(text):
    """Returns 'C ' followed by the text, replacing underscores with spaces"""
    return f"C {text.replace('_', ' ')}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
