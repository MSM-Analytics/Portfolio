import os
import sys
import pytest
from fastapi.testclient import TestClient

# 🔥 VARIÁVEIS DE AMBIENTE (ANTES DE IMPORTAR O APP)
os.environ["DB_HOST"] = "localhost"
os.environ["DB_PORT"] = "5432"
os.environ["DB_USER"] = "test"
os.environ["DB_PASSWORD"] = "test"
os.environ["DB_NAME"] = "test_db"
os.environ["ENV"] = "test"

# 🔥 PYTHONPATH
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

from app.main import app
from app.deps import get_current_user  # 👈 ESTE É O CARA CERTO


def override_get_current_user():
    return {
        "id": 1,
        "email": "test@test.com",
        "tenant_id": "test-tenant",
        "is_admin": True,
    }


@pytest.fixture(scope="module")
def client():
    app.dependency_overrides[get_current_user] = override_get_current_user

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
