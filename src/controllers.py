"""
This file contains the controller functions for handling HTTP requests in the application.
It includes functions for handling index page, HEI (Higher Education Institution) routes, and Entry routes.
Each function is documented with its purpose, parameters, and return values.
"""
from flask import current_app as app, request, make_response, jsonify
from sqlalchemy import exc
from marshmallow.exceptions import ValidationError

from src import db
from src.schemas import HEISchema, EntrySchema
from src.models import HEI, Entry


hei_schema = HEISchema()
heis_schema = HEISchema(many=True)
entry_schema = EntrySchema()
entries_schema = EntrySchema(many=True)


@app.route("/")
def index():
    """
    This function handles the index page request.

    Returns:
        str: The index page content.
    """
    app.logger.info("Index page requested")
    return "Index Page"

# HEI routes


@app.get("/hei")
def get_heis():
    """
    Retrieve a paginated list of HEIs (Higher Education Institutions).

    This function retrieves HEIs from the database based on the requested page number and number of items per page.
    It calculates the offset based on the requested page and per_page values.
    Then it queries the database to fetch the corresponding HEIs.
    The results are then serialized using the `heis_schema` and returned.

    Returns:
        JSON: A paginated list of HEIs in JSON format.

    Raises:
        ValidationError: If there is a Marshmallow validation error while serializing the HEIs.
        exc.SQLAlchemyError: If there is a SQLAlchemy error while fetching the HEIs from the database.
    """
    try:
        # Get the requested page number, default to 1 if not provided
        page = int(request.args.get('page', 1))
        # Get the number of items per page, default to 10 if not provided
        per_page = int(request.args.get('per_page', 10))

        # Calculate the offset based on the requested page and per_page values
        offset = (page - 1) * per_page
        all_heis = db.session.execute(
            db.select(HEI).offset(offset).limit(per_page)).scalars()
        try:
            result = heis_schema.dump(all_heis)

            return result
        except ValidationError as e:
            app.logger.error(
                f'A Marshmallow validation error occurred dumping regions: {str(e)}')
            msg = {
                'message': 'An Internal Server Error occurred. Please try again later.'}
            return make_response((msg), 500)
    except exc.SQLAlchemyError as e:
        app.logger.error(
            f'A SQLAlchemy error occurred fetching regions: {str(e)}')
        msg = {'message': 'An Internal Server Error occurred. Please try again later.'}
        return make_response((msg), 500)


@app.get("/hei/<ukprn>")
def get_hei_using_ukprn(ukprn):
    """
    Retrieves the Higher Education Institution (HEI) using the given UKPRN.

    Args:
        UKPRN (int): The UKPRN of the HEI.

    Returns:
        JSON: The JSON of the chosen HEI.

    Raises:
        exc.NoResultFound: If no HEI is found for the given UKPRN.

    """
    try:
        chosen_hei = db.session.execute(
            db.select(HEI).filter_by(UKPRN=ukprn)).scalar_one()
        return hei_schema.dump(chosen_hei)
    except exc.NoResultFound as e:
        app.logger.error(f'No result found for UKPRN: {
                         ukprn}. Error: {str(e)}')
        msg = {'message': f'No result found for UKPRN: {ukprn}'}
        return make_response((msg), 404)


@app.post("/hei")
def add_hei():
    """
    Add a new HEI (Higher Education Institution) to the database.

    Returns:
        JSON: JSON containing the success message if the HEI is added successfully,

    Raises:
        exc.SQLAlchemyError: If there is a SQLAlchemy error while adding the HEIs to the database.
        ValidationError: If there is a Marshmallow validation error while adding the HEI to the database.
    """
    hei_json = request.get_json()
    try:
        hei = hei_schema.load(hei_json)
        try:
            db.session.add(hei)
            db.session.commit()
            return {"message": f"HEI {hei.he_name} added successfully"}
        except exc.SQLAlchemyError as e:
            app.logger.error(
                f'A SQLAlchemy error occurred adding HEI: {str(e)}')
            msg = {
                'message': 'An Internal Server Error occurred. Please try again later.'}
            return make_response((msg), 500)
    except ValidationError as e:
        app.logger.error(
            f'A Marshmallow validation error occurred adding HEI: {str(e)}')
        msg = {'message': 'The HEI details failed validation.'}
        return make_response((msg), 400)


@app.delete("/hei/<ukprn>")
def delete_hei_using_ukprn(ukprn):
    """
    Deletes a Higher Education Institution (HEI) from the database using the provided UKPRN.

    Args:
        UKPRN (int): The UKPRN of the HEI to be deleted.

    Returns:
        JSON: A dictionary containing a message indicating the success or failure of the deletion.
    """
    try:
        hei = db.session.execute(db.select(HEI).filter(
            HEI.UKPRN == ukprn)).scalar_one()
        db.session.delete(hei)
        db.session.commit()
        return {"message": f"HEI {hei.UKPRN} deleted successfully"}
    except exc.SQLAlchemyError as e:
        app.logger.error(f'A SQLAlchemy error occurred deleting HEI: {str(e)}')
        msg = {'message': f'HEI with UKPRN {ukprn} not found.'}
        return make_response((msg), 404)


@app.route("/hei/<ukprn>", methods=['PUT', 'PATCH'])
def hei_update(ukprn):
    """
    Update the HEI (Higher Education Institution) with the given UKPRN (UK Provider Reference Number).

    Args:
        UKPRN (int): The UKPRN of the HEI to be updated.

    Returns:
        dict: A dictionary containing the success message if the update is successful.
              Otherwise, it returns an error message.

    Raises:
        exc.NoResultFound: If the HEI with the given UKPRN does not exist and it's a PATCH request.
        ValidationError: If the HEI details fail validation.
        exc.SQLAlchemyError: If a SQLAlchemy error occurs while updating the HEI.
    """
    # Check if the HEI exists
    try:
        hei = db.session.execute(db.select(HEI).filter(
            HEI.UKPRN == ukprn)).scalar_one()
    except exc.NoResultFound as e:
        # If the HEI doesn't exist and it's a PUT request, create a new HEI
        if request.method == 'PUT':
            app.logger.info(f'Creating a new HEI with UKPRN: {ukprn}')
            hei = HEI(UKPRN=ukprn)
        # If the HEI doesn't exist and it's a PATCH request, return a 404
        elif request.method == 'PATCH':
            app.logger.error(f'No result found for UKPRN: {
                             ukprn}. Error: {str(e)}')
            msg = {'message': f'No result found for UKPRN: {ukprn}'}
            return make_response(jsonify(msg), 404)
    hei_json = request.get_json()
    app.logger.info(f'Updating HEI with UKPRN: {ukprn} with data: {hei_json}')
    try:
        if request.method == 'PUT':
            # For PUT requests, replace the entire resource with the new data
            hei_update = hei_schema.load(hei_json)
        elif request.method == 'PATCH':
            # For PATCH requests, update only the specified fields
            hei_update = hei_schema.load(hei_json, instance=hei, partial=True)

    except ValidationError as e:
        app.logger.error(
            f'A Marshmallow validation error occurred updating HEI: {str(e)}')
        msg = {'message': 'The HEI details failed validation.'}
        return make_response(jsonify(msg), 400)
    try:
        # Check if UKPRN has been changed during the update
        if hei.UKPRN != hei_update.UKPRN:
            app.logger.info(f'Updating HEI with UKPRN: {
                            ukprn}. New UKPRN: {hei_update.UKPRN}')
        else:
            app.logger.info(f'Updating HEI with UKPRN: {ukprn}')

        # For both PUT and PATCH requests, add or update the resource in the database
        db.session.merge(hei_update)
        db.session.commit()
        app.logger.info(f'HEI with UKPRN {
                        hei_update.UKPRN} updated successfully')
        return {'message': f'HEI with UKPRN {hei_update.UKPRN} updated successfully'}

    except exc.SQLAlchemyError as e:
        app.logger.error(f'A SQLAlchemy error occurred updating HEI: {str(e)}')
        msg = {'message': 'An Internal Server Error occurred. Please try again later.'}
        return make_response(jsonify(msg), 500)

# Entry routes


@app.get("/entry")
def get_entries():
    """
    Returns:
        JSON: A paginated list of Entries in JSON format.

    Raises:
        ValidationError: If there is a Marshmallow validation error while serializing the Entries.
        exc.SQLAlchemyError: If there is a SQLAlchemy error while fetching the Entries from the database.
    """
    try:
        # Get the requested page number, default to 1 if not provided
        page = int(request.args.get('page', 1))
        # Get the number of items per page, default to 10 if not provided
        per_page = int(request.args.get('per_page', 10))

        # Calculate the offset based on the requested page and per_page values
        offset = (page - 1) * per_page

        all_entries = db.session.execute(
            db.select(Entry).offset(offset).limit(per_page)).scalars()
        try:
            result = entries_schema.dump(all_entries)

            return result
        except ValidationError as e:
            app.logger.error(
                f'A Marshmallow validation error occurred dumping entries: {str(e)}')
            msg = {
                'message': 'An Internal Server Error occurred. Please try again later.'}
            return make_response((msg), 500)
    except exc.SQLAlchemyError as e:
        app.logger.error(
            f'A SQLAlchemy error occurred fetching entries: {str(e)}')
        msg = {'message': 'An Internal Server Error occurred. Please try again later.'}
        return make_response((msg), 500)


@app.get("/entry/<id1>")
def get_entry(id1):
    """
    Retrieve an entry from the database based on the given ID.

    Args:
        id (int): The ID of the entry to retrieve.

    Returns:
        JSON: The serialized entry object.

    Raises:
        exc.NoResultFound: If no entry is found with the given ID.
    """
    try:
        one_entry = db.session.execute(
            db.select(Entry).filter_by(entry_id=id1)).scalar_one()
        return entry_schema.dump(one_entry)
    except exc.NoResultFound as e:
        app.logger.error(f'No result found for entry_id: {
                         id1}. Error: {str(e)}')
        msg = {'message': f'No result found for entry_id: {id1}'}
        return make_response((msg), 404)


@app.post("/entry")
def add_entry():
    """
    Add an entry to the database.

    Returns:
        JSON: A dictionary containing a success message if the entry is added successfully,
              or an error message if there is a validation error or a database error.
    """
    entry_json = request.get_json()
    try:
        entry = entry_schema.load(entry_json)
        try:
            db.session.add(entry)
            db.session.commit()
            return {"message": f"Entry {entry.entry_id} added successfully"}
        except exc.SQLAlchemyError as e:
            app.logger.error(
                f'A SQLAlchemy error occurred adding entry: {str(e)}')
            msg = {
                'message': 'An Internal Server Error occurred. Please try again later.'}
            return make_response((msg), 500)
    except ValidationError as e:
        app.logger.error(
            f'A Marshmallow validation error occurred adding entry: {str(e)}')
        msg = {'message': 'The entry details failed validation.'}
        return make_response((msg), 400)


@app.delete("/entry/<id1>")
def delete_entry(id1):
    """
    Deletes an entry from the database based on the given entry ID.

    Args:
        id1 (int): The ID of the entry to be deleted.

    Returns:
        dict: A dictionary containing a message indicating the success or failure of the deletion.
    """
    try:
        one_entry = db.session.execute(
            db.select(Entry).filter_by(entry_id=id1)).scalar_one()
        db.session.delete(one_entry)
        db.session.commit()
        return {"message": f"Entry {id1} deleted successfully"}
    except exc.SQLAlchemyError as e:
        app.logger.error(
            f'A SQLAlchemy error occurred deleting entry: {str(e)}')
        msg = {'message': f'Entry with id {id1} not found.'}
        return make_response((msg), 404)


@app.route("/entry/<id1>", methods=['PUT', 'PATCH'])
def entry_update(id1):
    """
    Update an entry with the given ID.

    Args:
        id1 (int): The ID of the entry to be updated.

    Returns:
        dict: A dictionary containing a message indicating the success or failure of the update.

    Raises:
        exc.NoResultFound: If no entry is found with the given ID.
        ValidationError: If the entry details fail validation.
        exc.SQLAlchemyError: If a SQLAlchemy error occurs during the update.
    """
    try:
        entry = db.session.execute(db.select(Entry).filter(
            Entry.entry_id == id1)).scalar_one()
    except exc.NoResultFound as e:
        if request.method == 'PUT':
            app.logger.info(f'Creating a new entry with id: {id1}')
            entry = Entry(entry_id=id1)
        elif request.method == 'PATCH':
            app.logger.error(f'No result found for entry_id: {
                             id1}. Error: {str(e)}')
            msg = {'message': f'No result found for entry_id: {id1}'}
            return make_response(jsonify(msg), 404)
    entry_json = request.get_json()
    app.logger.info(f'Updating entry with id: {id1} with data: {entry_json}')
    try:
        if request.method == 'PUT':
            entry_update = entry_schema.load(entry_json)
        elif request.method == 'PATCH':
            entry_update = entry_schema.load(
                entry_json, instance=entry, partial=True)
    except ValidationError as e:
        app.logger.error(
            f'A Marshmallow validation error occurred updating entry: {str(e)}')
        msg = {'message': 'The entry details failed validation.'}
        return make_response(jsonify(msg), 400)
    try:
        if entry.entry_id and entry.entry_id != entry_update.entry_id:
            app.logger.info(f'Updating entry with id: {
                            id1}. New id: {entry_update.entry_id}')
        else:
            app.logger.info(f'Updating entry with id: {id1}')

        db.session.merge(entry_update)
        db.session.commit()

        app.logger.info(f'Entry with entry_id {
                        entry_update.entry_id} updated successfully')
        return {'message': f'Entry with entry_id {entry_update.entry_id} updated successfully'}
    except exc.SQLAlchemyError as e:
        app.logger.error(
            f'A SQLAlchemy error occurred updating entry: {str(e)}')
        msg = {'message': 'An Internal Server Error occurred. Please try again later.'}
        return make_response(jsonify(msg), 500)
