import pytest

def test_index_page(client):
    """
    GIVEN a Flask test client
    WHEN a GET request is made to /
    THEN the status code should be 200
    AND the page should contain HTML that reads 'Index Page'
    """
    response = client.get('/')
    assert response.status_code == 200
    assert b'Index Page' in response.data

def test_404_page(client):
    """
    GIVEN a Flask test client
    WHEN a GET request is made to a non-existent page
    THEN the status code should be 404
    AND the page should contain HTML that reads 'Not Found'
    """
    response = client.get('/non-existent-page')
    assert response.status_code == 404
    assert b'Not Found' in response.data

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

# def test_get_hei(client):
#     """
#     GIVEN a Flask test client
#     WHEN a GET request is made to /hei
#     THEN the status code should be 200
#     AND the page should contain JSON data
#     """
#     response = client.get('/hei')
#     assert response.status_code == 200
#     assert response.is_json

# def test_get_specific_hei(client):
#     """
#     GIVEN a Flask test client
#     WHEN a GET request is made to /hei/10007788
#     THEN the status code should be 200
#     AND the page should contain JSON data
#     AND the UKPRN of the response should equal 10007788
#     """
#     response = client.get('/hei/10007788')
#     assert response.status_code == 200
#     assert response.is_json
#     assert response.json['UKPRN'] == 10007788

# def test_get_hei_nonexistent(client):
#     """
#     GIVEN a Flask test client
#     WHEN a GET request is made to /hei/12345678
#     THEN the status code should be 404
#     AND the page should contain HTML that reads 'Not Found'
#     """
#     response = client.get('/hei/12345678')
#     assert response.status_code == 404
#     assert response.json == {'message': 'No result found for UKPRN: 12345678'}

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

