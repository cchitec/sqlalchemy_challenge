import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    """Available api routes."""
    return(
        f"<b>API routes:</b> <p>"
        f" <a href=" + url + "/api/v1.0/precipitation target='_blank'>" + "/api/v1.0/precipitation" + "</a> <p>"
        f" <a href=" + url + "/api/v1.0/stations target='_blank'>" + "/api/v1.0/stations" + "</a> <p>"
        f" <a href=" + url + "/api/v1.0/tobs target='_blank'>" + "/api/v1.0/tobs" + "</a> <p>"
        f" <a href=" + url + "/api/v1.0/YYYY-MM-DD target='_blank'>" + "/api/v1.0/YYYY-MM-DD" + "</a> <p>"
        f" <a href=" + url + "/api/v1.0/YYYY-MM-DD/YYYY-MM-DD target='_blank'>" + "/api/v1.0/YYYY-MM-DD/YYYY-MM-DD" + "</a> <p>"
        )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    session = Session(engine)

    prcp_data = session.query(measurement.date, measurement.prcp).all()

    prcp_dict = {date:prcp for date,prcp in prcp_data}

    session.close()

    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def station():
 
    session = Session(engine)

    station_query = session.query(Station.station, Station.name).all()

    station_data = {station:name for station,name in station_query}

    session.close()

    return jsonify(station_data)

@app.route("/api/v1.0/tobs")
def tobs():
    
    session = Session(engine)
    
    latest = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    year_ago = dt.datetime.strptime(latest[0],'%Y-%m-%d') - dt.timedelta(days=365)


    act_station = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()
    
    tobs_query = session.query(measurement.date, measurement.tobs).filter(measurement.date >= year_ago).all()

    tobs_data = {date:tobs for date, tobs in tobs_query}

    return jsonify(tobs_data)

@app.route(f"/api/v1.0/<start_date>")
def start_date():
    
    session = Session(engine)
    
    end = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    start = dt.datetime.strptime(latest[0],'%Y-%m-%d') - dt.timedelta(days=365)

    tmin = func.min(measurement.tobs)

    tmax = func.max(measurement.tobs)

    tavg = func.avg(measurement.tobs)

    query = session.query(tmin, tmax, tavg).filter(measurement.date >= start).all()

    session.close()

    return jsonify(query)

@app.route(f"/api/v1.0/<start_date>/<end_date>")
def start_end():
    
    session = Session(engine)
    
    end = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    end = dt.datetime.strptime(end_date, '%Y-%m-%d')
   
    start = dt.datetime.strptime(latest[0],'%Y-%m-%d') - dt.timedelta(days=365)
    
    query = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).all()
    
    session.close()

    return jsonify(query)

if __name__ == '__main__':
    app.run(debug=True)

