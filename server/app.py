# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake(id):
    # Query the database for the earthquake with the specified id using filter_by and first
    earthquake = Earthquake.query.filter_by(id=id).first()

    if earthquake:
        # If found, return the earthquake data as JSON
        return jsonify({
            "id": earthquake.id,
            "location": earthquake.location,
            "magnitude": earthquake.magnitude,
            "year": earthquake.year
        }), 200
    else:
        # If not found, return a 404 status with an error message
        return jsonify({"message": f"Earthquake {id} not found."}), 404
    
@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    
    # Prepare the list of earthquake data
    quakes = [
        {
            "id": quake.id,
            "location": quake.location,
            "magnitude": quake.magnitude,
            "year": quake.year
        }
        for quake in earthquakes
    ]
    
    # Return the count and the list of earthquakes as a JSON response
    return jsonify({
        "count": len(quakes),
        "quakes": quakes
    }), 200   


if __name__ == '__main__':
    app.run(port=5555, debug=True)

