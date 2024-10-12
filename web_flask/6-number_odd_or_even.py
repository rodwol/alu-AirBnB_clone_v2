#!/usr/bin/python3
"""  starts a Flask web application """
from flask import Flask, render_template

app = Flask(__name__)


# Route for "/"
@app.route('/', strict_slashes=False)
def hello_hbnb():
    return "Hello HBNB!"


# Route for "/hbnb"
@app.route('/hbnb', strict_slashes=False)
def hbnb():
    return "HBNB"


# Route for "/c/<text>"
@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    return "C {}".format(text.replace('_', ' '))


# Route for "/python/(<text>)" with default value for text
@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text):
    return "Python {}".format(text.replace('_', ' '))


# Route for "/number/<n>" with validation for integer
@app.route('/number/<int:n>', strict_slashes=False)
def number_n(n):
    return "{} is a number".format(n)


# Route for "/number_template/<n>" to display HTML if n is integer
@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    return render_template('5-number.html', n=n)


# Route for "/number_odd_or_even/<n>" to display HTML if n is integer
@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n):
    return render_template('6-number_odd_or_even.html', n=n)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

