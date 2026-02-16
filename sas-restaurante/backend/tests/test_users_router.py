from unittest.mock import patch
from app.modules.gestao.schemas.user import UserListItem


def test_list_users_success(client):
    # 🔹 Dados fake retornados pelo service
    fake_users = [
        UserListItem(
            id=1,
            email="a@test.com",
            tenant_id="test-tenant",
            is_admin=False,
        ),
        UserListItem(
            id=2,
            email="b@test.com",
            tenant_id="test-tenant",
            is_admin=False,
        ),
    ]

    # 🔹 Mock do service (ANTES da request)
    with patch("app.modules.gestao.api.router.UserService.from_user") as service_mock:
        service_instance = service_mock.return_value
        service_instance.list_users.return_value = (fake_users, 2)

        response = client.get("/gestao/users?skip=0&limit=10")

    # 🔹 Asserts
    assert response.status_code == 200

    body = response.json()
    assert "items" in body
    assert "total" in body
    assert body["total"] == 2
    assert len(body["items"]) == 2
