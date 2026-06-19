from passlib.context import CryptContext
import os 
from datetime import datetime, timedelta
from typing import Union, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from dotenv import load_dotenv

from app import crud
from app.database import get_db

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = 30 # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 *24 * 7 # 7 days 
ALGORITHM = "HS256"
SECRET_KEY = os.getenv('JWT_SECRET_KEY')   # should be kept secret
REFRESH_SECRET_KEY = os.getenv('JWT_REFRESH_SECRET_KEY')   # should be kept secret

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_hashed_password(password: str)->str:
    """Takes a plain password and returns the hash for it so that
    it can be safely stored in the database."""
    return password_context.hash(password)

def verify_password(password: str, hashed_pass: str) -> bool:
    """Takes both the plain and the hashed passwords and 
    returns a boolean representing whether the two passwords
    match or not."""
    return password_context.verify(password, hashed_pass)

def create_access_token(subject: Union[str, Any], expires_delta: int = None)->str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, 
                 "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode,
                             SECRET_KEY, 
                             ALGORITHM)
    return encoded_jwt

def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def get_current_user(
    token: str = Depends(oauth2_scheme),
    conn=Depends(get_db),
):
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_error
    except JWTError as exc:
        raise credentials_error from exc

    user = crud.find_user(conn, email)
    if user is None:
        raise credentials_error
    return user
