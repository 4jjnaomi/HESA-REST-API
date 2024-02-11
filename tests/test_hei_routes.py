import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy.exc import SQLAlchemyError
from marshmallow.exceptions import ValidationError


def test_get_hei_contains_UKPRN(client):
    """
    GIVEN a Flask test client
    WHEN a GET request is made to /hei
    THEN the status code should be 200
    AND the page should contain JSON data
    AND the JSON data should have 8 digit values for UKPRN for all entries
    """
    response = client.get('/hei')
    assert response.status_code == 200
    assert response.is_json
    for hei in response.json:
        assert len(str(hei['UKPRN'])) == 8

@pytest.mark.parametrize('endpoint, expected_status_code, expected_data', [
    ('/hei', 200, None),  # No need to check data for /hei route
    ('/hei/10007788', 200, {'UKPRN': 10007788}),
    ('/hei/12345678', 404, {'message': 'No result found for UKPRN: 12345678'})
])

def test_get_hei_endpoints(client, endpoint, expected_status_code, expected_data):
    """
    GIVEN a Flask test client
    WHEN a GET request is made to various HEI endpoints
    THEN the status code and response data should match the expectations
    """
    response = client.get(endpoint)
    assert response.status_code == expected_status_code
    if expected_data is not None:
        assert response.is_json
        if 'UKPRN' in expected_data:  # Check only UKPRN for the second endpoint
            assert response.json['UKPRN'] == expected_data['UKPRN']
        else:  # Check all fields for other endpoints
            assert response.json == expected_data

def test_post_hei(client):
    """
    GIVEN a Flask test client
    WHEN a POST request is made to /hei with a JSON payload
    THEN the status code should be 200
    """
    response_json = {
        "UKPRN": 11111111,
        "he_name": "University of Me",
        "region": "London"
    }
    response = client.post('/hei', json=response_json, content_type='application/json')
    assert response.status_code == 200

def test_post_hei_invalid(client):
    """
    GIVEN a Flask test client
    WHEN a POST request is made to /hei with an invalid JSON payload
    THEN the status code should be 400
    """
    response_json = {
        "UKPRN": 11111111,
    }
    response = client.post('/hei', json=response_json, content_type='application/json')
    assert response.status_code == 400
    assert response.json == {'message': 'The HEI details failed validation.'}

def test_delete_hei(client, new_hei):
    """
    GIVEN a Flask test client
    WHEN a DELETE request is made to /hei/10000000
    THEN the status code should be 200
    """
    ukprn = new_hei['UKPRN']
    response = client.delete(f'/hei/{ukprn}')
    assert response.status_code == 200
    assert response.json == {"message": f"HEI {ukprn} deleted successfully"}

def test_delete_hei_nonexistent(client):
    """
    GIVEN a Flask test client
    WHEN a DELETE request is made to /hei/12345678
    THEN the status code should be 404
    """
    response = client.delete('/hei/12345678')
    assert response.status_code == 404
    assert response.json == {'message': 'HEI with UKPRN 12345678 not found.'}

def test_patch_hei(client, new_hei):
    """
    GIVEN a Flask test client
    WHEN a PATCH request is made to /hei/10000000 with a JSON payload
    THEN the status code should be 200
    """
    ukprn = new_hei['UKPRN']
    response_json = {
        "he_name": "Updated University",
        "region": "Updated Region"
    }
    response = client.patch(f'/hei/{ukprn}', json=response_json, content_type='application/json')
    assert response.status_code == 200
    assert response.json == {"message": f"HEI with UKPRN {ukprn} updated successfully"}

def test_patch_hei_nonexistent(client):
    """
    GIVEN a Flask test client
    WHEN a PATCH request is made to /hei/12345678 with a JSON payload
    THEN the status code should be 404
    """
    response_json = {
        "he_name": "Updated University",
        "region": "Updated Region"
    }
    response = client.patch('/hei/12345678', json=response_json, content_type='application/json')
    assert response.status_code == 404
    assert response.json == {'message': 'No result found for UKPRN: 12345678'}

def test_patch_hei_invalid(client, new_hei):
    """
    GIVEN a Flask test client
    WHEN a PATCH request is made to /hei/10000000 with an invalid JSON payload
    THEN the status code should be 400
    """
    ukprn = new_hei['UKPRN']
    response_json = {
        "name": "Updated University",
    }
    response = client.patch(f'/hei/{ukprn}', json=response_json, content_type='application/json')
    assert response.status_code == 400
    assert response.json == {'message': 'The HEI details failed validation.'}

def test_put_new_hei(client):
    """
    GIVEN a Flask test client
    WHEN a PUT request is made to /hei/10000001 with a JSON payload
    THEN the status code should be 201
    """
    response_json = {
        "UKPRN": 10000001,
        "he_name": "Other New University",
        "region": "London"
    }
    response = client.put('/hei/10000001', json=response_json, content_type='application/json')
    assert response.status_code == 200
    assert response.json == {"message": "HEI with UKPRN 10000001 updated successfully"}

def test_put_existing_hei(client, new_hei):
    """
    GIVEN a Flask test client
    WHEN a PUT request is made to /hei/10000000 with a JSON payload
    THEN the status code should be 200
    """
    ukprn = new_hei['UKPRN']
    response_json = {
        "UKPRN": ukprn,
        "he_name": "Putted University",
        "region": "Putted Region"
    }
    response = client.put(f'/hei/{ukprn}', json=response_json, content_type='application/json')
    assert response.status_code == 200
    assert response.json == {"message": f"HEI with UKPRN {ukprn} updated successfully"}

@patch('src.controllers.db.session.execute', side_effect=SQLAlchemyError)
def test_get_hei_exception(mock_execute, client):
    """
    GIVEN a Flask test client
    WHEN a GET request is made to /hei
    THEN the status code should be 500
    """
    response = client.get('/hei')
    assert response.status_code == 500
    assert response.json == {'message': 'An Internal Server Error occurred. Please try again later.'}

@patch('src.controllers.db.session.add', side_effect=SQLAlchemyError)
def test_post_hei_exception(mock_add, client):
    """
    GIVEN a Flask test client
    WHEN a POST request is made to /hei
    THEN the status code should be 500
    """
    response_json = {
        "UKPRN": 11111111,
        "he_name": "University of Me",
        "region": "London"
    }
    response = client.post('/hei', json=response_json, content_type='application/json')
    assert response.status_code == 500
    assert response.json == {'message': 'An Internal Server Error occurred. Please try again later.'}

@patch('src.controllers.db.session.merge', side_effect=SQLAlchemyError)
def test_patch_hei_exception(mock_merge, client, new_hei):
    """
    GIVEN a Flask test client
    WHEN a PATCH request is made to /hei/10000000
    THEN the status code should be 500
    """
    ukprn = new_hei['UKPRN']
    response_json = {
        "he_name": "Updated University",
        "region": "Updated Region"
    }
    response = client.patch(f'/hei/{ukprn}', json=response_json, content_type='application/json')
    assert response.status_code == 500
    assert response.json == {'message': 'An Internal Server Error occurred. Please try again later.'}

