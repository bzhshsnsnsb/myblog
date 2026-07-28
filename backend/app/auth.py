import base64
import hashlib
import hmac
import json
import os
import secrets
import time

from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


SECRET = os.getenv("BLOG_SECRET", "replace-this-secret-in-production")
USERNAME = os.getenv("ADMIN_USERNAME", "admin")
PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
TOKEN_TTL = 60 * 60 * 24
security = HTTPBearer(auto_error=False)


def _password_hash(password: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200_000)


def verify_credentials(username: str, password: str) -> bool:
    if not secrets.compare_digest(username, USERNAME):
        return False
    salt = hashlib.sha256((SECRET + USERNAME).encode()).digest()
    return secrets.compare_digest(_password_hash(password, salt), _password_hash(PASSWORD, salt))


def create_token(username: str) -> str:
    payload = base64.urlsafe_b64encode(json.dumps({"sub": username, "exp": int(time.time()) + TOKEN_TTL}).encode()).decode()
    signature = hmac.new(SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return f"{payload}.{signature}"


def require_admin(credentials: HTTPAuthorizationCredentials | None = Security(security)) -> str:
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="请先登录")
    try:
        payload, signature = credentials.credentials.rsplit(".", 1)
        expected = hmac.new(SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()
        data = json.loads(base64.urlsafe_b64decode(payload.encode()))
        valid = secrets.compare_digest(signature, expected) and data["exp"] > time.time()
    except (ValueError, KeyError, json.JSONDecodeError):
        valid = False
    if not valid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="登录已失效")
    return data["sub"]

