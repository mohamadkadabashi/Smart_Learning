from datetime import datetime, timedelta, timezone
from typing import Any, Dict

import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer
from config.setting import settings

# Password-Hasher
password_hasher = PasswordHash.recommended()

# === JWT-Config ===
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# OAuth2 Scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

def hash_password(plain_password: str) -> str:
    """
    Hashes a plain password using pwdlib.
    :plain_password: The plain password to hash.
    :return: The hashed password.
    """
    return password_hasher.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain password against a hashed password.

    :plain_password: The plain password to verify.
    :hashed_password: The hashed password to compare against.
    :return: True if the password matches, False otherwise.
    """
    return password_hasher.verify(plain_password, hashed_password)


def create_access_token(
    data: Dict[str, Any],
    expires_delta: timedelta | None = None,
) -> str:
    """
    Creates a JWT access token with an expiration time.

    :data: The data to include in the token payload.
    :expires_delta: Optional timedelta for token expiration.
    :return: The encoded JWT access token.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """
    Decodes a JWT access token and returns the payload.

    :token: The JWT access token to decode.
    :return: The decoded token payload.
    """
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload


def is_token_invalid_error(exc: Exception) -> bool:
    """
    Checks if the given exception is an InvalidTokenError.

    :exc: The exception to check.
    :return: True if the exception is an InvalidTokenError, False otherwise.
    """
    return isinstance(exc, InvalidTokenError)
