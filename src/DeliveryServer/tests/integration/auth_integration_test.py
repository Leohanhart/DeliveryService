from fastapi.testclient import TestClient
import pytest

from DeliveryServer.models.db.user_model.user_model import User
from DeliveryServer.server.server import app
from DeliveryServer.utils.database_connection import db_connection

client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    with db_connection() as session:
        # Delete user
        existing_user = (
            session.query(User).filter_by(username="testcreateuser").first()
        )
        if existing_user:
            # If the user exists, delete them
            session.delete(existing_user)
            session.commit()

        # Check if the user already exists in the database based on username, password, and role
        exists = (
            session.query(User.id).filter_by(username="testuser").first()
            is None
        )
        if exists:
            # Insert the necessary user data into the database
            user = User(
                username="testuser", password="testpassword", role="USER"
            )
            session.add(user)
            session.commit()


def test_register():
    # Define test data
    test_register_data = {
        "username": "testcreateuser",
        "password": "testcreatepassword",
    }

    # Make a request to the register endpoint
    response = client.post("auth/register", json=test_register_data)

    # Check response status code
    assert response.status_code == 201

    # Check response body
    response_data = response.json()
    assert "access_token" in response_data


def test_register_existing_user():
    # Assuming "testuser" already exists in the database
    existing_user_data = {"username": "testuser", "password": "testpassword"}

    # Send a request to register the existing user
    response = client.post("auth/register", json=existing_user_data)

    # Check response status code
    assert response.status_code == 409

    # Check response error message
    assert response.json()["detail"] == "This username is already being used!"


def test_login_successful():
    # Define test data
    test_login_data = {"username": "testuser", "password": "testpassword"}

    # Make a request to the login endpoint
    response = client.post("auth/login", json=test_login_data)

    # Check response status code
    assert response.status_code == 200

    # Check response body
    response_data = response.json()
    assert "access_token" in response_data


def test_login_invalid_credentials():
    # Define test data with invalid credentials
    invalid_login_data = {
        "username": "invaliduser",
        "password": "invalidpassword",
    }

    # Make a request to the login endpoint with invalid credentials
    response = client.post("auth/login", json=invalid_login_data)

    # Check response status code
    assert response.status_code == 401

    # Check response body
    assert response.json()["detail"] == "Incorrect username or password"
