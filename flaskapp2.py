import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
from flask import session
from datetime import datetime
import datetime as dt
import pandas as pd

engine = create_engine("sqlite:///C:\\Users\\JESICA\\hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app=Flask(__name__)

@app.route("/")
def home():
    return(
        f"Welcome! to my app <br/>"
        f"Available routes:<br/>"
        f"----------------------------<br/>"
        f"HOME (/)<br/>"
        f"To see precipitation by date /api/v1.0/precipitation<br/>"
        f"To retrieve the list of stations /api/v1.0/stations<br/>"
        f"To see data of temperature /api/v1.0/tobs<br/>"
        f"To see  the minimum temperature, the average temperature, and the max temperature /api/v1.0/start <br/>"
        f"To see  the minimum temperature, the average temperature, and the max temperature /api/v1.0/start/end <br/>"
        f"----------------------------<br/>"
    )   
@app.route("/api/v1.0/precipitation")
def precipitationres():
    precip= session.query(Measurement.date, Measurement.prcp).all()
    precipitation_list = []
    for date, prcp in precip:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        precipitation_list.append(precip_dict)
    return jsonify(precipitation_list)
    
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stat= session.query(Station.name).all()
    session.close()
    stations = list(np.ravel(stat))
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    last_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    year_before = dt.date(2017,8,23) - dt.timedelta(days=365)
    temp=session.query(Measurement.date,Measurement.tobs).\
      filter(Measurement.date > year_before).\
      order_by(Measurement.date).all()
    session.close()

    temperature=[]
    for tobs in temp:
        tob={}
        tob["date"]=temp[0]
        tob["tobs"]=temp[1]
        temperature.append(tob)

    return jsonify(temperature)

@app.route("/api/v1.0/start")
def inicio():

    session = Session(engine) 
    start_date=dt.date(2017,5,23)
    last_year = dt.timedelta(days=365)
    start = start_date-last_year
    end = dt.date(2017,8,23)
    trip_info= session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date < end).all()
    tripbeg = list(np.ravel(trip_info))
    session.close()
    return jsonify(tripbeg)

@app.route("/api/v1.0/start/end")
def fin():

    session = Session(engine) 
    start_date=dt.date(2017,5,23)
    last_year = dt.timedelta(days=365)
    start = start_date-last_year
    end = dt.date(2017,8,23)
    trip_info= session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    tripfin = list(np.ravel(trip_info))
    session.close()
    return jsonify(tripfin)

if __name__ == "__main__":

    app.run(debug=True)
