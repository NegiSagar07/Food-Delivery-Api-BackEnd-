from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.tasks.email_tasks import send_welcome_email
from ..schemas import UserCreate, UserRead, Token, TokenData
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..models import User
from sqlmodel import select
from ..security import get_password_hash, verify_password, create_access_token


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserRead)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # check if the user already exist
    query = await db.execute(select(User).where(User.email == user.email))
    db_user = query.scalars().first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email already exist")
    
    hashed_password = get_password_hash(user.password)

    new_user = User(
        name = user.name,
        email = user.email,
        hashed_password = hashed_password
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    send_welcome_email.delay(user_email=new_user.email, user_name=new_user.name)

    return new_user


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):

    query = await db.execute(select(User).where(User.email == form_data.username))
    user = query.scalars().first()

    if not user or not verify_password(user.hashed_password, form_data.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data = {"sub" : user.email})
    return {"access_token": access_token, "token_type": "bearer"}

