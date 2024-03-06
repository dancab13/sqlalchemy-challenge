# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
# 1.0 Create the engine.
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# 2.0 Reflect an existing database into a new model.
Base = automap_base()

# 3.0 Reflect the tables.
Base.prepare(autoload_with=engine)

# 4.0 Save references to each table.
Measurement = Base.classes.measurement
Station = Base.classes.station

# 5.0 Create our session (link) from Python to the DB.
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # 1.0 Create our session (link) from Python to the DB
    session = Session(engine)

    # 2.0 Query all dates and precipitation data
    precip = session.query(Measurement.date, Measurement.prcp)\
        .filter(Measurement.date >= '2016-08-23')\
        .all()

    session.close()

    # 3.0 Convert the query results from your precipitation analysis\ 
    # (i.e. retrieve only the last 12 months of data) to a dictionary\ 
    # using date as the key and prcp as the value.

    # 3.1 Create a dictionary from the row data
    precipitation_dict = {}
    for date, prcp in precip:
        precipitation_dict[date] = prcp

    # 4.0 Return the results in a JSON format.
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    # 1.0 Create our session (link) from Python to the DB
    session = Session(engine)

    # 2.0 Query all station names
    station_names = session.query(Measurement.station).all()
    
    # 3.0 Close the session.
    session.close()

    # 4.0 Return a JSON list of stations from the dataset.

    # 4.1 Iterate through the query and return values to a new list.
    stations_list = []
    for name in station_names:
        stations_list.append(name)

    # 4.2 Return the results in a JSON format.
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # 1.0 Create our session (link) from Python to the DB
    session = Session(engine)

    # 2.0 Query the dates and temperature observations of the most-active station\ 
    # for the previous year of data.

    # 2.1 Query the stations to find the one with the most rows of data.
    station_activity = session.query(Measurement.station, func.count(Measurement.station))\
        .group_by(Measurement.station)\
        .order_by(func.count(Measurement.station).desc())\
        .all()
    
    # 2.2 Select the first result from the list above; that is the most active station.
    most_active = station_activity[0]
    
    # 2.3 Query all of the dates and temp observations.
    # Note: The date is from a previous query that found\ 
    # the date a year prior from the station's most recent date
    year_temps = session.query(Measurement.date, Measurement.tobs)\
        .filter(Measurement.station == most_active)\
        .filter(Measurement.date >= '2016-08-18')\
        .all()
    
    # 3.0 Close the session.
    session.close()

    # 4.0 Return a JSON list of stations from the dataset.

    # 4.1 Iterate through the row data and append it to a list
    year_temps_list = []
    for date, temp in year_temps:
        year_temps_list.append(date, temp)

    # 4.2 Return the results in a JSON format.
    return jsonify(year_temps_list)

@app.route("/api/v1.0/<start>")
def start_route(start):
    # 1.0 Create our session (link) from Python to the DB
    session = Session(engine)

    # 2.0 Return a JSON list of the minimum temperature, the average temperature,\
    # and the maximum temperature for a specified start date.

    # 2.1 Get an input for the start date, which must be equal to or prior to the most recent date.
    

    # 2.2 Query the data to get the min, avg, and max temps.
    start_temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
        .filter(Measurement.date >= start_date)\
        .all()
    
    # 3.0 Close the session.
    session.close()

    # 4.0 Return a JSON list of stations from the dataset.

    # 4.1 Iterate through the row data and append it to a list
    start_temps_list = []
    for min, avg, max in start_temps:
        start_temps_list.append(min, avg, max)

    # 4.2 Return the results in a JSON format.
    return jsonify(start_temps_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end():
    # 1.0 Create our session (link) from Python to the DB
    session = Session(engine)

    # 2.0 Return a JSON list of the minimum temperature, the average temperature,\
    # and the maximum temperature for a specified start-end range.

    # 2.1 Get an input for the start date, which must be equal to or prior to the most recent date.
    start_date = input('Please enter a start date as YYYY-MM-DD.')

    if start_date == '%YYYY-%MM-%DD':
        print(f'The start date is {start_date}')
    else:
        print('Sorry, please enter a date in the YYYY-MM-DD format.')

    end_date = input('Please enter an end date as YYYY-MM-DD.')

    if end_date == '%YYYY-%MM-%DD':
        print(f'The end date is {end_date}')
    else:
        print('Sorry, please enter a date in the YYYY-MM-DD format.')

    # 2.2 Query the data to get the min, avg, and max temps.
    start_end_temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
        .filter(Measurement.date >= start_date)\
        .filter(Measurement.date <= end_date)\
        .all()
    
    # 3.0 Close the session.
    session.close()

    # 4.0 Return a JSON list of stations from the dataset.

    # 4.1 Iterate through the row data and append it to a list
    start_end_temps_list = []
    for min, avg, max in start_end_temps:
        start_end_temps_list.append(min, avg, max)

    # 4.2 Return the results in a JSON format.
    return jsonify(start_end_temps_list)

if __name__ == '__main__':
    app.run(debug=True)