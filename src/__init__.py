"""
This module initializes the Flask application and defines the database models and routes.

It imports necessary modules and sets up the Flask application with configuration settings.
The SQLAlchemy database and Marshmallow are also initialized.
The module includes a function to add data from CSV files to the database tables.
There is also a function to configure logging for the application.

Note: This module assumes that the CSV files are located in the 
'data' directory within the parent directory of the current 
file.
"""
import os
import csv
import logging

from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    This is the base class for the application.
    """
    pass


db = SQLAlchemy(model_class=Base)

ma = Marshmallow()


def add_data_from_csv():
    """
    Adds data from CSV files to the database.

    This function reads data from two CSV files, 'hei_data.csv' and 'entry_data.csv',
    and inserts the data into the corresponding database tables, HEI and Entry.

    If the database tables are empty, the function will read the CSV files and insert
    the data into the tables. Otherwise, it will skip the insertion step.

    Note: This function assumes that the CSV files are located in the 'data' directory
    within the parent directory of the current file.

    Args:
        None

    Returns:
        None
    """

    from src.models import HEI, Entry

    first_hei = db.session.execute(db.select(HEI)).first()
    if not first_hei:
        data_file = Path(__file__).parent.parent.joinpath(
            'data', 'hei_data.csv')
        with open(data_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                he = HEI(UKPRN=row[0], he_name=row[1],
                         region=row[2], lat=row[3], lon=row[4])
                db.session.add(he)
            db.session.commit()

    first_entry = db.session.execute(db.select(Entry)).first()
    if not first_entry:
        data_file = Path(__file__).parent.parent.joinpath(
            'data', 'entry_data.csv')
        with open(data_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                entry = Entry(entry_id=row[0], academic_year=row[1], classification=row[2],
                              category_marker=row[3], category=row[4], value=row[5], UKPRN=row[6], he_name=row[7])
                db.session.add(entry)
            db.session.commit()


def create_app(test_config=None):
    """
    Create and configure the Flask application.

    Args:
        test_config (dict, optional): Configuration dictionary for testing. Defaults to None.

    Returns:
        Flask: The Flask application instance.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='hEdmZaBc28fe_dHMm0QaXg',
        SQLALCHEMY_DATABASE_URI="sqlite:///" +
        os.path.join(app.instance_path, 'hei_environmental.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    configure_logging(app)

    db.init_app(app)

    ma.init_app(app)

    from src.models import HEI, Entry, User, SavedChart

    with app.app_context():
        db.create_all()

        add_data_from_csv()

        from src import controllers

    return app


def configure_logging(app):
    """ Configures Flask logging to a file.

    Logging level is set to DEBUG when testing which generates more detail.
    """
    logging.basicConfig(
        format='[%(asctime)s] %(levelname)s %(name)s: %(message)s')

    if app.config['TESTING']:
        logging.getLogger().setLevel(logging.DEBUG)
        handler = logging.FileHandler('src_tests.log')  # Log to a file
    else:
        logging.getLogger().setLevel(logging.INFO)
        handler = logging.FileHandler('src.log')  # Log to a file

    app.logger.addHandler(handler)
