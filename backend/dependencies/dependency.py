from typing import Annotated

from fastapi import Depends, HTTPException, status
import jwt 
from jwt import InvalidTokenError

from db.database import SessionDep
from models.user import User
from config.auth import SECRET_KEY, ALGORITHM, oauth2_scheme


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: SessionDep,
) -> User:
    """
    Retrieves the current user based on the provided JWT token.
    
    :token: The JWT token from the request.
    :session: The database session dependency.
    :return: The current authenticated User.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    user = session.get(User, int(user_id))
    if user is None:
        raise credentials_exception

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
