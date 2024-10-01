from fastapi import APIRouter, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer

from DeliveryServer.services.auth_service.auth_service import AuthService
from DeliveryServer.services.user_service.user_service import UserService
from DeliveryServer.services.questionnaire_service.questionnaire_service import (
    QuestionnaireService,
)


class UserRouter:
    router = APIRouter(
        prefix="/user",
        tags=["user"],
        responses={404: {"description": "Not found"}},
    )

    @router.get("/self")
    async def get_self(request: Request):
        """
        Get user information based on the provided access token.

        Returns:
            dict: User information (e.g., user ID, name, etc.).

        Raises:
            HTTPException: If the access token is invalid or unauthorized.
        """
        try:
            user = AuthService().check_access_token(request=request)

            return user
        except HTTPException:
            raise HTTPException(status_code=401, detail="Unauthorized")

    @router.get("/recommendation")
    async def get_recommendations_for_user(
        request: Request, test: str = "quick"
    ):
        """
        Get test recommendations for a user.

        Args:
            test (str, optional): Type of test (quick or advanced). Defaults to "quick".

        Returns:
            dict: Test recommendations for the user.

        Raises:
            HTTPException: If the access token is invalid or unauthorized.
            ValueError: If there are no test results for the user.
        """
        try:
            user = AuthService().check_access_token(request=request)

            if test == "quick":
                return QuestionnaireService().get_testresult_for_user(
                    user_id=user.id
                )

            elif test == "advanced":
                return
            else:
                return
        except HTTPException:
            raise HTTPException(status_code=401, detail="Unauthorized")
        except ValueError:
            raise HTTPException(
                status_code=404,
                detail="There are no test results for this user.",
            )

    @router.get("/test")
    async def get_test_id_for_user(request: Request) -> list[dict]:
        """
        Get test IDs associated with a user.

        Returns:
            list[dict]: List of test IDs (as dictionaries) for the user.

        Raises:
            HTTPException: If the access token is invalid or unauthorized.
            ValueError: If there are no tests for the user.
        """
        try:
            user = AuthService().check_access_token(request=request)

            return QuestionnaireService().get_test_id_for_user(user_id=user.id)
        except HTTPException:
            raise HTTPException(status_code=401, detail="Unauthorized")
        except ValueError:
            raise HTTPException(
                status_code=404, detail="There are no tests for this user."
            )
