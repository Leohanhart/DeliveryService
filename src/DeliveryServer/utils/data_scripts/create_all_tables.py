# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 12:38:57 2024

@author: Gebruiker
"""
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker

from DeliveryServer.models.db.user_model.user_model import Base as BaseUser

from DeliveryServer.utils.database_connection import server, engine


def create_if_not_exists():
    """
    create all inserted tables if not exists

    Returns
    -------
    None.

    """
    # here the bases of the models declaird.
    server.start()

    inspector = inspect(engine)

    # Check if stockticker tables need to be declared.
    if not inspector.has_table("user"):
        # Create a session using a context manager (with statement)
        with sessionmaker(bind=engine)() as session:
            # Create the tables
            BaseUser.metadata.create_all(bind=engine)
    server.stop()


if __name__ == "__main__":
    # Your main code here
    create_if_not_exists()
