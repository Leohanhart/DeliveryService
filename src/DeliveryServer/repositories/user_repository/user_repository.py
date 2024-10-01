from sqlalchemy.orm import Session
import hashlib


from DeliveryServer.models.db.user_model.user_model import User
from DeliveryServer.models.dto.auth_dto.auth_dto import LoginDTO, RegisterDTO
from DeliveryServer.models.dto.user_dto.user_dto import ReturnUserDTO
from DeliveryServer.utils.exceptions.exeptions import (
    UsernameAlreadyExists,
    NotFound,
)


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_user(self, register_dto: RegisterDTO, role):
        """
        Create the user in the database

            Parameters:
                register_dto (RegisterDTO): The username a password a user wants to use
                role (str): The role the user should have
        """
        user_already_exists = (
            self.session.query(User.id)
            .filter_by(username=register_dto.username)
            .first()
            is not None
        )
        if user_already_exists:
            raise UsernameAlreadyExists

        user = User(
            username=register_dto.username,
            password=register_dto.password,
            role=role,
        )
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

    def check_user(self, login_dto: LoginDTO) -> str:
        """
        Check if the user exists and return the role of the user

        Parameters:
            login_dto (LoginDTO): The username and password a user wants to use

        Returns:
            (str): The role of the user
        """
        user = (
            self.session.query(User)
            .filter(User.username == login_dto.username)
            .first()
        )
        if user:
            # Hashing the provided password for comparison
            hashed_password = hashlib.sha256(
                login_dto.password.encode()
            ).hexdigest()
            if user.password == hashed_password:
                return user.role
        raise NotFound

    def get_user_by_username(self, username: str) -> ReturnUserDTO:
        result = (
            self.session.query(User).filter(User.username == username).first()
        )
        user = ReturnUserDTO(
            id=result.id, username=result.username, role=result.role
        )

        return user
