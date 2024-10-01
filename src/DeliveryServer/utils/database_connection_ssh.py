from sshtunnel import SSHTunnelForwarder
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
from loguru import logger
import time

# Load environment variables from the .env file
load_dotenv()

# Access the environment variables
ssh_host = os.getenv("SSH_HOST")
ssh_port = int(os.getenv("SSH_PORT", 22))
ssh_user = os.getenv("SSH_USER")
ssh_password = os.getenv("SSH_PASSWORD")

db_host = os.getenv("DB_HOST")
db_port = int(os.getenv("DB_PORT", 5433))
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_database = os.getenv("DB_DATABASE")
db_name = os.getenv("DB_DATABASE")

server = SSHTunnelForwarder(
    (ssh_host, ssh_port),
    ssh_username=ssh_user,
    ssh_password=ssh_password,
    remote_bind_address=(db_host, db_port),
)
server.start()

db_url = f"postgresql://{db_user}:{db_password}@127.0.0.1:{server.local_bind_port}/{db_name}"
engine = create_engine(db_url, echo=False)


class db_connection:
    """
    DbConnection is a context manager class that facilitates a secure connection to a PostgreSQL database
    through an SSH tunnel using SSHTunnelForwarder and SQLAlchemy.

    Example usage:

        with db_connection() as session:

            # Your code using the SQLAlchemy session goes here

            result = session.execute(text("SELECT * FROM users"))
            for row in result:
                logger.debug(row)


    """

    def __init__(
        self,
    ):
        """
        Nothing

        Parameters
        ----------
         : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        self.ssh_host = ssh_host
        self.ssh_port = ssh_port
        self.ssh_user = ssh_user
        self.ssh_password = ssh_password
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.server = None
        self.turn_off_after_connection: bool = (
            False  # turn on if the connection need to be closed after use.
        )

    def __enter__(self):
        try:
            self.server = server

            # startup connection

            if not self.server.tunnel_is_up:
                self.server.start()

            self.db_url = f"postgresql://{self.db_user}:{self.db_password}@127.0.0.1:{self.server.local_bind_port}/{self.db_name}"
            engine = create_engine(self.db_url, echo=False, pool_size=10)
            Session = sessionmaker(bind=engine)
            self.session = Session()

            return self.session

        except Exception as e:
            raise ConnectionError(e)

    def __exit__(self, exc_type, exc_value, traceback):
        if hasattr(self, "session") and self.session:
            self.session.close()
        if self.server and self.turn_off_after_connection:
            self.server.stop()


def test_connection():
    """

    test connection with SSH tunnel.


    Returns
    -------
    TYPE / BOOL : True or False
        DESCRIPTION.

    """
    try:
        logger.debug(ssh_host, ssh_port, ssh_user, ssh_password, db_host, db_port)
        with SSHTunnelForwarder(
            (ssh_host, ssh_port),
            ssh_username=ssh_user,
            ssh_password=ssh_password,
            remote_bind_address=(db_host, db_port),
        ) as server:
            server.start()

            local_port = str(server.local_bind_port)
            engine = create_engine(
                f"postgresql://{db_user}:{db_password}@127.0.0.1:{local_port}/{db_database}"
            )

            Session = sessionmaker(bind=engine)
            session = Session()

            # Test data retrieval
            test = session.execute(text("SELECT 1"))
            result = test.scalar()  # Try to retrieve a single value

            session.close()

            return result is not None

    except Exception as e:
        logger.debug(f"Connection failed: {str(e)}")
        return False


if __name__ == "__main__":
    while True:
        with db_connection() as session:
            start_time = time.time()
            # Your code using the SQLAlchemy session goes here
            result = session.execute(text("SELECT * FROM users"))
            for row in result:
                logger.debug(row)
            end_time = time.time()
            elapsed_time = end_time - start_time
            logger.debug(f"Elapsed time: {elapsed_time} seconds")