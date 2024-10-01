from DeliveryServer.utils.database_connection import (
    db_connection,
    test_connection,
)


def test_db_connection():
    # Test that the context manager works correctly
    with db_connection() as session:
        assert session is not None
        # You can add more assertions here to test the session object or any other behavior


def test_test_connection():
    # Test the connection using SSHTunnelForwarder
    status = test_connection()
    assert (
        status  # You might need to adjust this based on the expected behavior
    )
