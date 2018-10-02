import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import sqlite3

import warnings
warnings.filterwarnings('ignore')

from flask import Flask, jsonify


# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
#conn = sqlite3.connect('../Resrouces/hawaii.sqlite', check_same_thread=False)

# Create base
Base = automap_base()

# reflect tables
Base.prepare(engine, reflect=True)
#Base.classes.keys()

# Save references to the measurement and station tables
Measurement=Base.classes.measurement
Station=Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


# Flask Setup
app = Flask(__name__)


# Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes: <br/>"
        f"<a href= " "/api/v1.0/precipitation </a><br/>" "Precipitation"+
        f"<a href= " "/api/v1.0/stations </a> <br/>" "Stations" +
        f"<a href= " "/api/v1.0/tobs </a> <br/>" "Temperature Observations" +
        f"<a href= " "/api/v1.0/start </a> <br>" "Start End"
    )

    

@app.route("/api/v1.0/precipitation")
def precipitation():
       
    prcp_results = session.query(Measurement.date, Measurement.prcp).\
                   filter(Measurement.date.between('2016-07-01', '2017-07-01')).all()

    prev_prcp = []
    for prcp in prcp_results:
        prcp_dict = {}
        prcp_dict["Date"] = Measurement.date
        prcp_dict["Prcp"] = Measurement.prcp
        prev_prcp.append(prcp_dict)
    return jsonify(prev_prcp)

@app.route("/api/v1.0/stations")
def stations():
    """List Stations"""
    
    station_results = session.query(Station.station).all()
    all_stations = list(np.ravel(station_results))
    
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """List: temperature for last year (one year shifted) """

    tobs_results = session.query(Measurement.station, Measurement.tobs).filter(Measurement.date.between('2016-10-01', '2017-10-01')).all()
    
    tobs_list=[]
    for tobs in tobs_results:
        tobs_dict = {}
        tobs_dict["station"] = tobs[0]
        tobs_dict["tobs"] = tobs[1]
       
        tobs_list.append(tobs_dict)
        
    return jsonify(tobs_list)

@app.route("/api/v1.0/start")

def calc_temps(start='start_date'):
    start_date = datetime.strptime('2017-07-01', '%Y-%m-%d').date()
    start_results = session.query(func.max(Measurement.tobs), \
                            func.min(Measurement.tobs),\
                            func.avg(Measurement.tobs)).\
                            filter(Measurement.date >= start_date) 
    
    start_tobs = []
    for tobs in start_results:
        tobs_dict = {}
        tobs_dict["TAVG"] = tobs[2]
        tobs_dict["TMAX"] = tobs[0]
        tobs_dict["TMIN"] = tobs[1]
        
        start_tobs.append(tobs_dict)

    return jsonify(start_tobs)


if __name__ == '__main__':
    app.run(debug=True)
