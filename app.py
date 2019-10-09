import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

#flask Setup
app = Flask(__name__)

#flast routes

#route 1
@app.route("/")
def home():
    return (f"Here are the routes:<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
    )

#route 2
@app.route("/api/v1.0/precipitation")
def prcp():

    one_year = dt.date(2017,8,23) - dt.timedelta(days=365)

    data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= one_year).\
    order_by(Measurement.date).all()

    prcp_app = {date: prcp for date, prcp in data}

    return jsonify(prcp_app)

#route 3
@app.route("/api/v1.0/stations")
def stations():

    station_list = session.query(Station.station).all()

    return jsonify(station_list)

#route 4
@app.route("/api/v1.0/tobs")
def tobs():

    one_year = dt.date(2017,8,23) - dt.timedelta(days=365)

    data2 = session.query(Measurement.tobs).\
    filter(Measurement.station == "USC00519281").\
    filter(Measurement.date >= one_year).all()

    return jsonify(data2)

#Define main behavior
if __name__ == "__main__":
    app.run(debug=True)