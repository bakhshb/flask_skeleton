"""
This file (test_tasks.py) contains the functional tests for the tasks blueprint.

These tests use GETs and POSTs to different URLs to check for the proper behavior
of the tasks blueprint.
"""

def test_task_all(test_client, logged_in_user):
    """
    GIVEN a Flask application
    WHEN the '/task/all' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/task/all')
    assert response.status_code == 200
    assert b"created_from" in response.data
    assert b"created_to" in response.data
    assert b"search" in response.data
    assert b"First Name" in response.data
    assert b"Last Name" in response.data
    assert b"Task Type" in response.data
    assert b"Organization" in response.data
    assert b"Place" in response.data
    assert b"Task From" in response.data
    assert b"Task To" in response.data
    assert b"Result" in response.data
    assert b"created at" in response.data
    assert b"search" in response.data

def test_task_create(test_client, logged_in_user):
    """
    GIVEN a Flask application
    WHEN the '/task/add' page is requested (GET)
    THEN check the response is valid
    """

    response = test_client.post('/task/task/type/add', data=dict(name='meeting'), follow_redirects=True)
    assert response.status_code == 200
    response = test_client.post('/task/organization/add', data=dict(name='ministry'),follow_redirects=True)
    assert response.status_code == 200
    response = test_client.post('/task/place/add', data=dict(name='jeddah'),follow_redirects=True)
    assert response.status_code == 200
    response = test_client.post('/task/add', data=dict(user_id='1', task_type_id='1', organization_id='1', place_id='1'),follow_redirects=True)
    assert response.status_code == 200
    assert b"meeting" in response.data
    assert b"ministry" in response.data
    assert b"jeddah" in response.data

def test_task_search (test_client, logged_in_user):
    response = test_client.get('/task/search')
    assert response.status_code == 200
    assert b"created_from" in response.data
    assert b"created_to" in response.data
    assert b"search" in response.data
