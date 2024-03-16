"""
Testing utils.py
"""

import pytest
from starlette.testclient import TestClient

from utils import init_app, init_model, not_completed


def test_init_app():
    """
    Testing the init_app function.
    """
    app = init_app()
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Running Hello, World!"}


def test_cors_preflight_request():
    """
    Testing the CORS preflight request.
    It has to fail because the origin is not allowed.
    """
    app = init_app()
    client = TestClient(app)
    # Simulate a preflight request
    response = client.options(
        "/",
        headers={
            "Origin": "http://example.com",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code == 400
    assert "Disallowed CORS origin" in response.text


def test_cors_request():
    """
    Testing the CORS request.
    Has to pass because the origin is allowed.
    """
    app = init_app()
    client = TestClient(app)
    # Simulate a preflight request
    response = client.options(
        "/",
        headers={
            "Origin": "http://localhost:8080",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:8080"


def test_cors_request_3000():
    """
    Testing the CORS request.
    Has to pass because the origin is allowed.
    """
    app = init_app()
    client = TestClient(app)
    # Simulate a preflight request
    response = client.options(
        "/",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"
    assert response.headers["access-control-allow-credentials"] == "true"


def test_hello_world():
    """
    Testing the hello_world function.
    """
    app = init_app()
    client = TestClient(app)
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}


def test_not_completed():
    """
    Testing the not_completed decorator.
    """

    @not_completed
    def dummy_function():
        pass

    with pytest.warns(UserWarning) as record:
        dummy_function()

    assert len(record) == 1
    assert "'dummy_function' is marked as not completed" in str(record[0].message)


def test_init_model() -> None:
    """
    Testing the init_model function.
    """
    classifier, tokenizer = init_model()

    assert classifier.num_labels == 2
    assert (
        classifier.device.type == "cuda" if classifier.device.type == "cuda" else "cpu"
    )

    assert tokenizer.pad_token_id == 0
    assert len(tokenizer.added_tokens_decoder) == 5

    list_tokens: list[str] = [
        "[PAD]",
        "[CLS]",
        "[SEP]",
        "[UNK]",
        "[MASK]",
    ]

    for _, decoder in tokenizer.added_tokens_decoder.items():
        assert decoder.content in list_tokens
