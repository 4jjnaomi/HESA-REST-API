import os
import csv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase
from pathlib import Path

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

ma = Marshmallow()

def add_data_from_csv():

    from src.models import HEI, Entry

    first_HEI = db.session.execute(db.select(HEI)).first()
    if not first_HEI:
        data_file = Path(__file__).parent.parent.joinpath('data', 'hei_data.csv')
        with open(data_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                he = HEI(UKPRN=row[0], he_name=row[1], region=row[2], lat=row[3], lon=row[4])
                db.session.add(he)
            db.session.commit()

    first_entry = db.session.execute(db.select(Entry)).first()
    if not first_entry:
        data_file = Path(__file__).parent.parent.joinpath('data', 'entry_data.csv')
        with open(data_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                entry = Entry(entry_id=row[0], academic_year=row[1], classification=row[2], category_marker=row[3], category=row[4], value=row[5], UKPRN=row[6], he_name=row[7])
                db.session.add(entry)
            db.session.commit()

def create_app(test_config=None):
    # create the Flask app
    app = Flask(__name__, instance_relative_config=True)
    # configure the Flask app (see later notes on how to generate your own SECRET_KEY)
    app.config.from_mapping(
        SECRET_KEY='hEdmZaBc28fe_dHMm0QaXg',
        # Set the location of the database file called paralympics.sqlite which will be in the app's instance folder
        SQLALCHEMY_DATABASE_URI= "sqlite:///" + os.path.join(app.instance_path, 'hei_environmental.sqlite'),  
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    db.init_app(app)

    ma.init_app(app)

    from src.models import HEI, Entry, User, SavedChart

    with app.app_context():
        db.create_all()

        add_data_from_csv()

        from src import controllers

    return app

