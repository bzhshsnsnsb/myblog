import os
from pathlib import Path

TEST_DB = Path(__file__).parent / "test.db"
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB.as_posix()}"

from fastapi.testclient import TestClient

from app.database import engine
from app.main import app


def test_blog_flow():
    with TestClient(app) as client:
        health = client.get("/api/health")
        assert health.status_code == 200

        articles = client.get("/api/articles").json()
        assert articles["total"] >= 4
        slug = articles["items"][0]["slug"]

        detail = client.get(f"/api/articles/{slug}")
        assert detail.status_code == 200

        comment = client.post(
            f"/api/articles/{slug}/comments",
            json={"author": "测试读者", "email": "reader@example.com", "content": "这是一条测试留言。"},
        )
        assert comment.status_code == 201

        login = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
        assert login.status_code == 200
        token = login.json()["token"]
        admin = client.get("/api/admin/articles", headers={"Authorization": f"Bearer {token}"})
        assert admin.status_code == 200


def teardown_module():
    engine.dispose()
    if TEST_DB.exists():
        TEST_DB.unlink()
