"""
This module contains error handlers for handling exceptions and HTTP errors in a Flask application.
"""
from flask import json, current_app as app, jsonify
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import HTTPException

# ERROR HANDLERS


@app.errorhandler(Exception)
def handle_exception(e):
    """Handle non-HTTP exceptions as 500 Server error in JSON format.

    Args:
        e:  The Python base Exception class
    Returns:
        response:  A Flask HTTP response with JSON format 500 Server error
    """

    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return e

    # now you're handling non-HTTP exceptions only
    return jsonify(error=str(e)), 500


@app.errorhandler(HTTPException)
def handle_exception_http(e):
    """Return JSON instead of HTML for HTTP errors.

    Args:
        e: An HTTP exception
    Returns:
        response: A Flask response with the HTTP response in JSON format
    """
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


@app.errorhandler(ValidationError)
def register_validation_error(error):
    """Error handler for marshmallow schema validation errors.

    Args:
        error (ValidationError): Marshmallow error.

    Returns:
        HTTP response with the validation error message and the 400 status code
    """
    response = error.messages
    return response, 400


@app.errorhandler(404)
def not_found_error(e):
    """Error handler for 404 Not Found errors.

    Args:
        error: 404 Not Found error

    Returns:
        HTTP response with the 404 status code
    """
    return jsonify(error=str(e)), 404
