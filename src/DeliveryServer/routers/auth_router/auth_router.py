from fastapi import APIRouter, HTTPException

from DeliveryServer.models.dto.auth_dto.auth_dto import LoginDTO, RegisterDTO
from DeliveryServer.services.auth_service.auth_service import AuthService
from DeliveryServer.utils.exceptions.exeptions import (
    NotFound,
    UsernameAlreadyExists,
)


class AuthRouter:
    router = APIRouter(
        prefix="/auth",
        tags=["auth"],
        responses={
            404: {"description": "Not found"},
            401: {"description": "Unauthorized"},
        },
    )

    @router.post("/register", status_code=201)
    async def register(register_dto: RegisterDTO) -> dict:
        """
        The API endpoint to register a user

            Parameters:
                register_dto (RegisterDTO): The username a password a user wants to use

            Returns:
                (str): A access token for authenticaiton
        """
        try:
            auth_service = AuthService()
            default_role = "USER"
            auth_service.add_user(register_dto, default_role)
            return auth_service.generate_token(
                register_dto.username, default_role
            )
        except UsernameAlreadyExists:
            raise HTTPException(
                status_code=409, detail="This username is already being used!"
            )

    @router.post("/login")
    async def login(login_dto: LoginDTO) -> dict:
        """
        The API endpoint to login as a user

            Parameters:
                login_dto (loginDTO): The username a password for the account the user wants to login to

            Returns:
                (str): A access token for authenticaiton
        """
        try:
            auth_service = AuthService()

            return auth_service.login_user(login_dto)
        except NotFound:
            raise HTTPException(
                status_code=401, detail="Incorrect username or password"
            )
