"""
This module contains unit tests for the general routes of the Flask application.
"""
from src.models import User


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


def test_set_password():
    """
    GIVEN a User model
    WHEN the set_password method is called
    THEN it should set the password_hash field
    """
    u = User(email='test@example.com', password='password123')
    u.set_password('newpassword')

    assert u.password_hash is not None
    assert u.password_hash != 'newpassword'


def test_check_password():
    """
    GIVEN a User model
    WHEN the check_password method is called
    THEN it should return True if the password is correct
    AND False if it is not
    """
    u = User(email='test@example.com', password='password123')
    u.set_password('password123')

    assert u.check_password('password123')


def test_check_password_false():
    """
    GIVEN a User model
    WHEN the check_password method is called
    THEN it should return False if the password is incorrect
    """
    u = User(email='test@example.com', password='password123')
    u.set_password('password123')

    assert not u.check_password('wrongpassword')
