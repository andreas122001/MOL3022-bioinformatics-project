"""
This module contains the function to initialize and configure the FastAPI application.

The `init_app` function creates a new instance of the FastAPI application.
Configures it with CORS middleware.
The CORS middleware allows cross-origin requests from the specified origins.
For the development purposes, the origins are set to `http://localhost*`
Also for the development purposes, the middleware is configured to allow all methods and headers.

Example:
    app = init_app()
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def init_app() -> FastAPI:
    """
    Initializes and configures the FastAPI application.

    Returns:
        FastAPI: The initialized FastAPI application.
    """
    app = FastAPI()

    origins: list[str] = [
        "http://localhost",
        "http://localhost:8080",
        "http://localhost:3000",
    ]

    app.add_middleware(
        middleware_class=CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
