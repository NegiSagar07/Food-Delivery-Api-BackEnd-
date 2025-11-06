from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, VerifyMismatchError
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from sqlmodel import Session, select
from .models import User
from .config import settings
from typing import Optional


ph = PasswordHasher(
    time_cost=3, # time waste
    memory_cost=65536, # expensive gpu
    parallelism=4, 
    hash_len=32,
    salt_len=16
)


def get_password_hash(password):
    return ph.hash(password)


def verify_password(hashed_password, plain_password):
    try:
        ph.verify(hashed_password, plain_password)
        return True
    except (VerificationError, VerifyMismatchError):
        return False
    

def create_access_token(data: dict, expire_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expire_delta:
        expire = datetime.now(timezone.utc) + expire_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})

    token = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
    return token


def get_user_from_token(token: str, session: Session):
    # decode the token
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
        
        user = session.exec(select(User).where(User.email == email)).first()
        return user
    except JWTError:
        return None