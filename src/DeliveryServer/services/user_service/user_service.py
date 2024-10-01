from DeliveryServer.repositories.user_repository.user_repository import (
    UserRepository,
)
from DeliveryServer.models.dto.user_dto.user_dto import ReturnUserDTO
from DeliveryServer.utils.database_connection import db_connection


class UserService:
    def __init__(self):
        with db_connection() as session:
            self.user_repository = UserRepository(session)

    def get_user_by_username(self, username: str) -> ReturnUserDTO:
        return self.user_repository.get_user_by_username(username=username)
