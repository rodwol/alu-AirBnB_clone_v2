#!/usr/bin/python3
""" starts a Flask web application """
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def states():
    states = storage.all(State)
    return render_template('9-states.html', states=states, mode='all')


@app.route('/states/<id>', strict_slashes=False)
def state_cities(id):
    for state in storage.all(State).values():
        if state.id == id:
            return render_template('9-states.html', states=state, mode='one')
    return render_template('9-states.html', states=state, mode='none')


@app.teardown_appcontext
def teardown_db(exception):
    """Removes the current SQLAlchemy session after each request."""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
