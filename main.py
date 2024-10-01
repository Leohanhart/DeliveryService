import uvicorn


def main():
    """
    Boot up the application.

    Args:
        env (str): The environment to run the application in, can be one of "local",
        "dev", or "prod".
        debug (bool): Whether or not to run the application in debug mode.

    Returns:
        None
    """
    uvicorn.run(
        "src.DeliveryServer.server.server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        workers=20,
        limit_concurrency=1000,
    )


if __name__ == "__main__":
    main()
