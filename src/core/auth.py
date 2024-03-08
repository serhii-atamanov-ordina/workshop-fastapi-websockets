from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import get_database
from src.routers.users.controller import get_user_by_name

# Replace these values with your actual secret key and algorithm
SECRET_KEY = "workshop"
ALGORITHM = "HS256"

# OAuth2PasswordBearer with async support
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Function to decode JWT token
async def decode_token(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_database)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        name, password = payload.get("name"), payload.get("password")

        if not name:
            raise credentials_exception

        user = await get_user_by_name(name, session)

        if name != user.name or password != user.password:
            raise credentials_exception

    except JWTError:
        raise credentials_exception
    return name


if __name__ == "__main__":
    # Payload (data you want to include in the token)
    payload = {"name": "user", "password": "fastapi"}

    # Generate the token
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    print("Generated Token:", token)
