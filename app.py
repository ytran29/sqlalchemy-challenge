import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Database Setup
###########################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
print(Base.classes.keys)
Measurement = Base.classes.measurement
Station = Base.classes.station
###########################################################

#Flask setup
##########################################################
app = Flask(__name__)
##########################################################
@app.route("/")
def Welcome():
    """List all available api routes."""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    """Return a list of date and the recorded precipitation scores"""
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > '2016-08-23').\
        order_by(Measurement.date).all()
    session.close()

    precipitation_scores = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = prcp
        precipitation_scores.append(precipitation_dict)

    return jsonify(precipitation_scores)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    """Return a list of all stations"""
    results = session.query(Station.name).distinct().all()
    session.close()
    for name in results:
        return jsonify(results)
    
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    """Return a list of all recorded temperatures from the most active station"""
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >'2016-08-23').\
         filter(Measurement.station == 'USC00519281').all()
    session.close()
    recorded_temperatures = []
    for date, tobs in results:
        temperatures_dict = {}
        temperatures_dict["date"] = tobs
        recorded_temperatures.append(temperatures_dict)
    return jsonify(recorded_temperatures)

    
    

if __name__ == '__main__':
        app.run(debug=True)