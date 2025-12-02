# config/auth.py
from datetime import datetime, timedelta, timezone
from typing import Any, Dict

import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer
from config.setting import settings

# Passwort-Hasher (z.B. Argon2, empfohlen)
password_hasher = PasswordHash.recommended()

# === JWT-Config ===
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# OAuth2 Schema – tokenUrl zeigt auf deinen Login-Endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")

def hash_password(plain_password: str) -> str:
    return password_hasher.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hasher.verify(plain_password, hashed_password)


def create_access_token(
    data: Dict[str, Any],
    expires_delta: timedelta | None = None,
) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=15)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload


def is_token_invalid_error(exc: Exception) -> bool:
    return isinstance(exc, InvalidTokenError)
