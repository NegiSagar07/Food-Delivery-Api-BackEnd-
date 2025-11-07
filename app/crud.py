from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .models import User, Restaurant
from sqlmodel import select
from typing import Optional


async def get_user_by_email(email: str, db: AsyncSession) -> Optional[User]:
    query = select(User).where(User.email == email)
    user = await db.execute(query)
    return user.scalars().one_or_none()


async def get_restaurant_by_name(name: str, db: AsyncSession) -> Optional[Restaurant]:
    query = select(Restaurant).where(Restaurant.name == name)
    restaurant = await db.execute(query)
    return restaurant.scalars().one_or_none()


async def create_restaurant(name: str, rating: Optional[float], owner_id: int, db: AsyncSession) -> Restaurant:
    new_restaurant = Restaurant(
        name = name,
        rating = rating,
        owner_id = owner_id
    )
    db.add(new_restaurant)
    await db.commit()
    await db.refresh(new_restaurant)

    return new_restaurant