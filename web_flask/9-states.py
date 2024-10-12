#!/usr/bin/python3
""" starts a Flask web application """
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def states():
    states = storage.all(State).values()
    return render_template('9-states.html', states=states)

@app.route('/states/<id>', strict_slashes=False)
def state_cities(id):
    states = storage.all('State')
    state = "State.{}".format(id)
    
    if state:
        sorted_cities = sorted(state.cities, key=lambda city: city.name)
        return render_template('9-states.html', state=state, cities=sorted_cities)
    else:
        return render_template('not_found.html')

@app.teardown_appcontext
def teardown_db(exception):
    """Removes the current SQLAlchemy session after each request."""
    storage.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
