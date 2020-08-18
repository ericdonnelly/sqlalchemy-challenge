import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
app.config['DEBUG'] = True

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """Welcome to the Hawaii Climate API!"""
    return (
         f"Avalable Routes:<br/>"
         
         f"/api/v1.0/precipitation<br/>"
         f"- Dates and temperatures for the last year of precipitation data<br/>"
         
         f"/api/v1.0/stations<br/>"
         f"- List of all weather stations<br/>"

         f"/api/v1.0/tobs<br/>"
         f"- List of temperature observations (TOBS) from the previous year<br/>"

        f"/api/v1.0/start<br/>"
        f"- When given the start date (YYYY-MM-DD), calculates the MIN/AVG/MAX temperature for all dates greater than and equal to the start date<br/>"
        f"/api/v1.0/start/end<br/>"
        f"- When given the start and the end date (YYYY-MM-DD), calculate the MIN/AVG/MAX temperature for dates between the start and end date inclusive<br/>"
    )
    
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return dates and temperatures for the last year of precipitation data"""
    # Query precipitaton data
    results = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date >= "2016-08-23").\
    filter(measurement.date <= "2017-08-23").all()

    session.close()

    # Create a dictionary from the data and append to a list
    precipitation_data = []
    for row in results:
        precipitation_dict = {}
        precipitation_dict["date"] = row.date
        precipitation_dict["prcp"] = row.prcp
        precipitation_data.append(precipitation_dict)

    return jsonify(precipitation_data)

    
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """List of all weather stations """
    # Query all stations
    results = session.query(station.station).all()

    session.close()

    stations_data = list(np.ravel(results))
    
    return jsonify(stations_data)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """List of temperature observations (TOBS) from the previous year """
    # Query for all temperature observations from previous year
    results = session.query(measurement.tobs).all()

    session.close()

    # Convert list of tuples into normal list
    tobs_data = list(np.ravel(results))

    return jsonify(tobs_data)

@app.route("/api/v1.0/<start>")
def startdate(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Query min, avg, max for start range
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).all()

    session.close()

    # Convert list of tuples into normal list
    start_data = list(np.ravel(results))

    return jsonify(start_data)

@app.route("/api/v1.0/<start>/<end>")
def total_date(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Query min, avg, max, for start/end range
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).all()
    
    session.close()

    # Convert list of tuples into normal list
    start_end_data = list(np.ravel(results))

    return jsonify(start_end_data)


if __name__ == '__main__':
    app.run()
