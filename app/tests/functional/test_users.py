"""
This file (test_users.py) contains the functional tests for the users blueprint.

These tests use GETs and POSTs to different URLs to check for the proper behavior
of the users blueprint.
"""
def test_home_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/', follow_redirects=True)
    assert response.status_code == 200
    assert b"Please Login" in response.data
    assert b"Create Account" in response.data

def test_login_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/user/login' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/user/login')
    assert response.status_code == 200
    assert b"Please Login" in response.data
    assert b"Email" in response.data
    assert b"Password" in response.data
    assert b"Forgot" in response.data
    assert b"Password?" in response.data
    assert b"Login" in response.data
    assert b"Create Account" in response.data

def test_valid_login_logout(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/user/login' page is posted to (POST)
    THEN check the response is valid
    """
    response = test_client.post('/user/login',
                                data=dict(email='test1@gmail.com', password='FlaskIsAwesome'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"Hello, world!" in response.data
    assert b"This is a template for a simple marketing or informational website. It includes a large callout called a jumbotron and three supporting pieces of content. Use it as a starting point to create something more unique." in response.data
    assert b"Learn more" in response.data
    assert b"Logout" in response.data

    """
    GIVEN a Flask application
    WHEN the '/user/logout' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data
    assert b"Create Account" in response.data

def test_invalid_login(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/user/login' page is posted to with invalid credentials (POST)
    THEN check an error message is returned to the user
    """
    response = test_client.post('/user/login',
                                data=dict(email='test1@gmail.com', password='FlaskIsNotAwesome'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"Invalid password" in response.data
    assert b"Create Account" in response.data


def test_valid_registration(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/user/register' page is posted to (POST)
    THEN check the response is valid and the user is logged in
    """
    response = test_client.post('/user/register',
                                data=dict(firstname='test',
                                lastname='test',
                                email='test1@yahoo.com',
                                password='FlaskIsGreat',),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"test" in response.data
    assert b"test" in response.data
    assert b"test1@yahoo.com" in response.data



def test_invalid_registration(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/user/register' page is posted to with invalid credentials (POST)
    THEN check an error message is returned to the user
    """
    response = test_client.post('/user/register',
                                data=dict(email='patkennedy79@hotmail.com',
                                          password='FlaskIsGreat',
                                          confirm='FlskIsGreat'),   # Does NOT match!
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"Thanks for registering" not in response.data
    assert b"[This field is required.]" not in response.data
    assert b"Register" in response.data
