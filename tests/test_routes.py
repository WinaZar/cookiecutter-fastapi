from fastapi.testclient import TestClient

from backend.auth.utils import decode_jwt
from backend.config import Configuration
from backend.db.models import User


def test_auth_restrict(test_client: TestClient) -> None:
    with test_client as client:
        result = client.get("/ping")

    assert result.status_code == 401
    assert result.json() == {"detail": "Not authenticated"}


def test_obtain_token(
    test_client: TestClient, test_config: Configuration, user: User
) -> None:
    with test_client as client:
        result = client.post(
            "/token", data={"username": user.username, "password": "password"}
        )
    assert result.status_code == 200

    result_json = result.json()
    claims = decode_jwt(test_config, result_json["access_token"])
    assert result_json["token_type"] == "bearer"
    assert claims["username"] == user.username
    assert claims["sub"] == str(user.id)


def test_graphql_endpoint(test_client: TestClient, user: User, test_token: str):
    with test_client as client:
        result = client.post(
            "/graphql",
            json={
                "query": "query { users { id, username, is_active } }",
                "variables": None,
            },
            headers={"Authorization": f"Bearer {test_token}"},
        )
    assert result.status_code == 200
    assert result.json() == {
        "data": {
            "users": [
                {
                    "id": str(user.id),
                    "username": user.username,
                    "is_active": user.is_active,
                }
            ]
        }
    }
