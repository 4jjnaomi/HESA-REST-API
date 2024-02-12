"""
This module contains unit tests for the entry routes of a Flask application.
The tests cover various HTTP methods and endpoints related to entry operations,
such as getting entries, adding entries, updating entries, and deleting entries.
"""
from unittest.mock import patch
import pytest

from sqlalchemy.exc import SQLAlchemyError


def test_get_entries(client):
    """
    GIVEN a Flask test client
    WHEN a GET request is made to /entry
    THEN the status code should be 200
    AND the page should contain JSON data
    """
    response = client.get('/entry')
    assert response.status_code == 200
    assert response.is_json


@pytest.mark.parametrize('endpoint, expected_status_code, expected_data',
                         [
                            ('/entry/755', 200, {'entry_id': 755}),
                            ('/entry/999999', 404, {'message': 'No result found for entry_id: 999999'})
                            ])
def test_get_entry_endpoints(client, endpoint, expected_status_code, expected_data):
    """
    GIVEN a Flask test client
    WHEN a GET request is made to various Entry endpoints
    THEN the status code and response data should match the expectations
    """
    response = client.get(endpoint)
    assert response.is_json
    assert response.status_code == expected_status_code
    if 'entry_id' in expected_data:
        assert response.json['entry_id'] == expected_data['entry_id']
    else:
        assert response.json == expected_data


def test_add_entry(client):
    """
    GIVEN a Flask test client
    WHEN a POST request is made to /entry with a JSON payload
    THEN the status code should be 200
    """
    response_json = {
        "entry_id": "100000",
        "academic_year": "20/20",
        "classification": "dummy",
        "category_marker": "dummy",
        "category": "dummy",
        "value": "70",
        "UKPRN": "111111",
        "he_name": "University of Naomi"
    }
    response = client.post('/entry', json=response_json,
                           content_type='application/json')
    assert response.status_code == 200


def test_delete_entry(client, new_entry):
    """
    GIVEN a Flask test client and a new entry
    WHEN a DELETE request is made to '/entry/{entry_id}'
    THEN the status code should be 200
    AND the response JSON should match the expected message
    """
    entry_id = new_entry['entry_id']
    response = client.delete(f'/entry/{entry_id}')
    assert response.status_code == 200
    assert response.json == {"message": f"Entry {entry_id} deleted successfully"}


def test_delete_nonexistent_entry(client):
    """
    GIVEN a client
    WHEN a DELETE request is made to '/entry/999999' - a non-existent entry
    THEN ensure the response status code is 404
    AND ensure the response JSON matches the expected message
    """
    response = client.delete('/entry/999999')
    assert response.status_code == 404
    assert response.json == {'message': 'Entry with id 999999 not found.'}


def test_patch_entry(client, new_entry):
    """
    GIVEN a client and a new entry
    WHEN a PATCH request is made to '/entry/{entry_id}' with the updated entry JSON
    THEN ensure the response status code is 200
    AND ensure the response JSON matches the expected message
    """
    entry_id = new_entry['entry_id']
    response_json = {
        "academic_year": "21/22",
        "classification": "updated",
        "category_marker": "updated",
        "category": "updated",
        "value": "80",
        "UKPRN": "222222",
        "he_name": "Updated University"
    }
    response = client.patch(
        f'/entry/{entry_id}', json=response_json, content_type='application/json')
    assert response.status_code == 200
    assert response.json == {"message": f"Entry with entry_id {entry_id} updated successfully"}


def test_patch_nonexistent_entry(client):
    """
    GIVEN a client and a JSON payload for updating an non-existent entry
    WHEN a PATCH request is made to '/entry/123456' with the JSON payload
    THEN ensure the response status code is 404
    AND ensure the response JSON matches the expected message
    """
    response_json = {
        "academic_year": "21/22",
        "classification": "updated",
        "category_marker": "updated",
        "category": "updated",
        "value": "80",
        "UKPRN": "222222",
        "he_name": "Updated University"
    }
    response = client.patch(
        '/entry/123456', json=response_json, content_type='application/json')
    assert response.status_code == 404
    assert response.json == {'message': 'No result found for entry_id: 123456'}


def test_put_update_entry(client, new_entry):
    """
    GIVEN a client and a new entry JSON
    WHEN a PUT request is made to '/entry/{entry_id}' with the new entry JSON
    THEN ensure the response status code is 200
    AND ensure the response JSON matches the expected message
    """
    entry_id = new_entry['entry_id']
    response_json = {
        "entry_id": entry_id,
        "academic_year": "21/22",
        "classification": "updated",
        "category_marker": "updated",
        "category": "updated",
        "value": "80",
        "UKPRN": "222222",
        "he_name": "Updated University"
    }
    response = client.put(
        f'/entry/{entry_id}', json=response_json, content_type='application/json')
    assert response.status_code == 200
    assert response.json == {"message": f"Entry with entry_id {entry_id} updated successfully"}


def test_put_new_entry(client):
    """
    GIVEN a client and a new entry JSON
    WHEN a PUT request is made to '/entry/123456' with the new entry JSON
    THEN ensure the response status code is 200
    AND ensure the response JSON matches the expected message
    """
    response_json = {
        "entry_id": "123456",
        "academic_year": "21/22",
        "classification": "updated",
        "category_marker": "updated",
        "category": "updated",
        "value": "80",
        "UKPRN": "222222",
        "he_name": "Updated University"
    }
    response = client.put('/entry/123456', json=response_json,
                          content_type='application/json')
    assert response.status_code == 200
    assert response.json == {'message': 'Entry with entry_id 123456 updated successfully'}


@patch('src.controllers.db.session.execute', side_effect=SQLAlchemyError)
def test_get_entry_exception(mock_execute, client):
    """
    GIVEN a client
    WHEN a GET request is made to '/entry'
    THEN ensure the response status code is 500
    AND ensure the response JSON matches the expected message
    """
    response = client.get('/entry')
    assert response.status_code == 500
    assert response.json == {'message': 'An Internal Server Error occurred. Please try again later.'}


@patch('src.controllers.db.session.add', side_effect=SQLAlchemyError)
def test_post_entry_exception(mock_add, client):
    """
    GIVEN a client
    WHEN a POST request is made to '/entry' with a new entry JSON
    THEN ensure the response status code is 500
    AND ensure the response JSON matches the expected message
    """
    response_json = {
        "entry_id": "100000",
        "academic_year": "20/20",
        "classification": "dummy",
        "category_marker": "dummy",
        "category": "dummy",
        "value": "70",
        "UKPRN": "111111",
        "he_name": "University of Naomi"
    }
    response = client.post('/entry', json=response_json,
                           content_type='application/json')
    assert response.status_code == 500
    assert response.json == {'message': 'An Internal Server Error occurred. Please try again later.'}


@patch('src.controllers.db.session.merge', side_effect=SQLAlchemyError)
def test_patch_entry_exception(mock_merge, client, new_entry):
    """
    GIVEN a client, a mock_merge function, and a new_entry
    WHEN a PATCH request is made to '/entry/{entry_id}' with updated entry JSON
    THEN ensure the response status code is 500
    AND ensure the response JSON matches the expected message
    """
    entry_id = new_entry['entry_id']
    response_json = {
        "academic_year": "21/22",
        "classification": "updated",
        "category_marker": "updated",
        "category": "updated",
        "value": "80",
        "UKPRN": "222222",
        "he_name": "Updated University"
    }
    response = client.patch(
        f'/entry/{entry_id}', json=response_json, content_type='application/json')
    assert response.status_code == 500
    assert response.json == {'message': 'An Internal Server Error occurred. Please try again later.'}
