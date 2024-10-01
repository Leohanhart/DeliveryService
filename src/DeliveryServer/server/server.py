from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from DeliveryServer.routers.user_router.user_router import UserRouter
from DeliveryServer.routers.auth_router.auth_router import AuthRouter
from DeliveryServer.routers.job_router.job_router import JobRouter
from DeliveryServer.routers.questionnaire_router.questionnaire_router import (
    QuestionnaireRouter,
)

tags_metadata = [
    {
        "name": "auth",
        "description": "Operations for authentication including login and register.",
    }
]

app = FastAPI(
    openapi_tags=tags_metadata,
    title="Delivery Server",
    summary="""The backend of a application that enables users to get the data.""",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Delivery Team",
        "url": "https://localhost",
        "email": "test@test.nl",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(UserRouter.router)
app.include_router(AuthRouter.router)
app.include_router(JobRouter.router)
app.include_router(QuestionnaireRouter.router)


@app.route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def fallback_route(request: Request):
    """
    Fallback router for API if a non exiting endpoint is called

        Parameters:
            path (str): The path of the user

        Returns:
            Raises 404 exception
    """
    # Return a exeption indicating that the endpoint doesn't exist
    raise HTTPException(
        status_code=404,
        detail=f"This endpoint does not exist: {request.url}",
    )


if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        workers=20,
        limit_concurrency=1000,
    )
