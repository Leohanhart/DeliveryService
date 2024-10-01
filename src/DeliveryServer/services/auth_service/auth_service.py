import datetime
import os
from dotenv import load_dotenv
import hashlib

from fastapi import HTTPException, Request
import jwt

from DeliveryServer.models.dto.user_dto.user_dto import ReturnUserDTO
from DeliveryServer.services.user_service.user_service import UserService
from DeliveryServer.utils.database_connection import db_connection
from DeliveryServer.models.dto.auth_dto.auth_dto import LoginDTO, RegisterDTO
from DeliveryServer.repositories.user_repository.user_repository import (
    UserRepository,
)

# Load environment variables from the .env file
load_dotenv()

# Access the environment variables
sercret_key = os.getenv("SECRET_KEY")


class AuthService:
    def __init__(self):
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 720
        with db_connection() as session:
            self.user_repository = UserRepository(session)

    def add_user(self, register_dto: RegisterDTO, role: str):
        """
        Call function to create user in database

        Parameters:
            register_dto (RegisterDTO): The username a password a user wants to use
            role (str): The role the user should have
        """
        # Hashing the password
        register_dto.password = hashlib.sha256(
            register_dto.password.encode()
        ).hexdigest()

        # Creating user with hashed password
        self.user_repository.create_user(register_dto, role)

    # Generate JWT token with user roles
    def generate_token(self, username: str, role: str) -> dict:
        """
        Return a generates access token for the user

            Parameters:
                username (str): The username of the user
                role (str): The role the user should have

            Returns:
                (str): Access token of the user
        """
        expires = datetime.datetime.now() + datetime.timedelta(
            minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        payload = {"username": username, "role": role, "exp": expires}
        token = jwt.encode(payload, sercret_key, algorithm=self.ALGORITHM)
        return {"access_token": token}

    # Verify JWT token and extract user roles
    def verify_token(
        self,
        token: str,
        expected_roles: list = ["USER", "ADMIN"],
    ) -> tuple:
        """
        Check if user is authenticated

            Parameters:
                token (str): The accestoken of the user
                expected_roles (list): A list of the roles a user could have

            Returns:
                (str): The username of the user
                (str): The role of the user
        """
        try:
            payload = jwt.decode(
                token, sercret_key, algorithms=[self.ALGORITHM]
            )
            username = payload.get("username")
            role = payload.get("role")
            if username:
                if role in expected_roles:
                    return username, role
                else:
                    raise HTTPException(status_code=401, detail="Unauthorized")

            if role is None:
                raise HTTPException(status_code=401, detail="Unauthorized")
        except jwt.ExpiredSignatureError:
            pass
        except jwt.DecodeError:
            pass

        raise HTTPException(status_code=401, detail="Unauthorized")

    def login_user(self, login_dto: LoginDTO) -> dict:
        """
        Check if the user exits and generate acces token for the user

            Parameters:
                login_dto (LoginDTO): The username and password of the user

            Returns:
                (str): The access token for the user
        """
        role = self.user_repository.check_user(login_dto)

        if role is None:
            raise HTTPException(status_code=401, detail="Unauthorized")
        else:
            return self.generate_token(login_dto.username, role)

    # Generate JWT token endpoint
    def generate_token_endpoint(self, username: str, role: str) -> dict:
        """
        Call the generate token function and return the acces token

            Parameters:
                username (str): The username of the user
                role (str): The role the user should have

            Returns:
                access_token (str): Access token of the user
        """
        token = self.generate_token(username, role)
        return {"access_token": token}

    # Verify JWT token endpoint
    def verify_token_endpoint(self, token: str) -> dict:
        """
        Check if user is authenticated and check if the token has a username

            Parameters:
                token (str): The access token of the user

            Returns:
                valid (bool): The bool if the user is a valid user or not
                username(str): The username of the user
                role (str): The role of the user
        """
        username, role = self.verify_token(token)
        if username is None:
            return {"valid": False}
        return {"valid": True, "username": username, "role": role}

    def check_access_token(self, request: Request) -> ReturnUserDTO:
        access_token = request.headers.get("Authorization")

        auth = self.verify_token_endpoint(access_token)
        if not auth.get("valid"):
            raise HTTPException(status_code=401, detail="Unauthorized")

        user_service = UserService()
        user = user_service.get_user_by_username(auth.get("username"))
        return user
