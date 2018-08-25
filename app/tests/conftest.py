import pytest
from flask_skeleton import create_app
from flask_skeleton.model import db, User
from flask_login import login_user


@pytest.fixture(scope='module')
def new_user():
    user = User(firstname='admin',lastname='test',email='test@gmail.com', active=1)
    user.hash_password('FlaskIsAwesome')
    return user

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('test')

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()

@pytest.fixture(scope='module')
def init_database():
    # Create the database and the database table
    db.create_all()

    # Insert user data
    user1 = User(firstname='admin',lastname='test',email='test1@gmail.com', active=1)
    user1.hash_password('FlaskIsAwesome')
    user2 = User(firstname='user',lastname='test',email='test2@gmail.com')
    user2.hash_password('PaSsWoRd')
    db.session.add(user1)
    db.session.add(user2)

    # Commit the changes for the users
    db.session.commit()

    yield db  # this is where the testing happens!

    db.drop_all()

@pytest.fixture(scope='module')
def logged_in_user(test_client, init_database):
    # Log in 
    return test_client.post('/user/login',
                                data=dict(email='test1@gmail.com', password='FlaskIsAwesome'),
                                follow_redirects=True)
