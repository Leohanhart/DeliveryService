# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 11:54:00 2024

@author: Gebruiker
"""

import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from redis import Redis

# Load environment variables from .env file
load_dotenv()

# Retrieve PostgreSQL connection parameters from environment variables
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")
database = os.getenv("POSTGRES_DB")
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")

# Check if all PostgreSQL environment variables are set
if not all([host, port, database, user, password]):
    raise ValueError("Missing PostgreSQL environment variables.")

# Create a SQLAlchemy engine for PostgreSQL
db_url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
engine = create_engine(db_url, echo=False, pool_size=20)

# Retrieve PostgreSQL connection parameters for Datahub from environment variables
host_datahub = os.getenv("DATAHUB_POSTGRES_HOST")
port_datahub = os.getenv("DATAHUB_POSTGRES_PORT")
database_datahub = os.getenv("DATAHUB_POSTGRES_DB")
user_datahub = os.getenv("DATAHUB_POSTGRES_USER")
password_datahub = os.getenv("DATAHUB_POSTGRES_PASSWORD")

# Check if all Datahub PostgreSQL environment variables are set
if not all(
    [
        host_datahub,
        port_datahub,
        database_datahub,
        user_datahub,
        password_datahub,
    ]
):
    raise ValueError("Missing Datahub PostgreSQL environment variables.")

# Create a SQLAlchemy engine for Datahub
db_url_datahub = f"postgresql://{user_datahub}:{password_datahub}@{host_datahub}:{port_datahub}/{database_datahub}"
engine_datahub = create_engine(
    db_url_datahub, echo=False, pool_size=20, max_overflow=10
)

# Get Redis configuration from environment variables
redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")
redis_password = os.getenv("REDIS_PASSWORD")

# Check if all Redis environment variables are set
if not all([redis_host, redis_port, redis_password]):
    raise ValueError("Missing Redis environment variables.")

# Build the Redis URL
redis_url = f"redis://:{redis_password}@{redis_host}:{redis_port}/0"

# Establish a connection to the Redis server
r = Redis.from_url(redis_url, socket_connect_timeout=1)

# Optionally, you can also create a StrictRedis instance if needed
redis_client = Redis(
    host=redis_host,
    port=redis_port,
    password=redis_password,
    decode_responses=True,
)
