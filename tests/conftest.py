import os
from pathlib import Path

import pytest
from sqlalchemy import exists
from src import create_app, db
from src.models import HEI
from src.schemas import HEISchema


@pytest.fixture(scope='session')
def app():
    """Fixture that creates a test app.

    The app is created with test config parameters that include a temporary database. The app is created once for
    each test module.

    Returns:
        app A Flask app with a test config

    """
    # See https://flask.palletsprojects.com/en/2.3.x/tutorial/tests/#id2
    # Create a temporary testing database
    db_path = Path(__file__).parent.parent.joinpath('data', 'hei_environmental_testdb.sqlite')
    test_cfg = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///" + str(db_path),
    }
    app = create_app(test_config=test_cfg)

    # # Push an application context to bind the SQLAlchemy object to the application
    with app.app_context():
        db.create_all()

    yield app

    # # Clean up / reset resources
    with app.app_context():
        db.session.remove()  # Close the database session
        db.drop_all()

        # Explicitly close the database connection
        db.engine.dispose()

    # clean up / reset resources
    # Delete the test database (if adding data to your database takes a long time you may prefer not to delete the
    # database)

    os.unlink(db_path)


@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def new_hei(app):
    new_hei_json = {
        "UKPRN": 10000000,
        "he_name": "New Univerity",
        "region": "New Region"
    }
    with app.app_context():
        new_hei = HEISchema().load(new_hei_json)
        db.session.add(new_hei)
        db.session.commit()
        
    yield new_hei_json

    with app.app_context():
            hei_exists = db.session.query(exists().where(HEI.UKPRN == "10000000")).scalar()
            if hei_exists:
                # Only delete the HEI if it exists in the database
                db.session.execute(HEI.__table__.delete().where(HEI.UKPRN == "10000000"))
                db.session.commit()
