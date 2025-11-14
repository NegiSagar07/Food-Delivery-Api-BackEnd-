from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .models import User, Restaurant, Food, RestaurantFoodLink, Order
from sqlmodel import select
from typing import Optional, List
from .schemas import MenuLinkUpdate

# ------User Crud------

async def get_user_by_email(email: str, db: AsyncSession) -> Optional[User]:
    query = select(User).where(User.email == email)
    user = await db.execute(query)
    return user.scalars().one_or_none()


# ------Restaurant Crud------

async def get_restaurant_by_id(restaurant_id: int, db: AsyncSession) -> Optional[Restaurant]:
    """
    Fetch a single restaurant by its ID.
    """
    query = select(Restaurant).where(Restaurant.id == restaurant_id)
    result = await db.execute(query)
    return result.scalars().one_or_none()


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


async def get_restaurant(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Restaurant]:
    query = select(Restaurant).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def get_restaurant_menu(restaurant_id: int, db: AsyncSession) -> List[RestaurantFoodLink]:
    query = select(RestaurantFoodLink).where(RestaurantFoodLink.restaurant_id == restaurant_id)
    result = await db.execute(query)
    return result.scalars().all()


# ------Food Crud------

async def creat_food(name: str, description: Optional[str], db: AsyncSession) -> Food:
    new_food = Food(name = name, description = description)
    db.add(new_food)
    await db.commit()
    await db.refresh(new_food)

    return new_food


async def get_food_by_id(id: int, db:AsyncSession) -> Optional[Food]:
    query = select(Food).where(Food.id == id)
    food = await db.execute(query)
    return food.scalars().one_or_none()


async def get_food_by_name(name: str, db: AsyncSession) -> Optional[Food]:
    query = select(Food).where(Food.name == name)
    food = await db.execute(query)

    return food.scalars().one_or_none()


# ------Menu Crud------

async def add_item_to_menu(restaurant_id: int, food_id: int, price: float, db: AsyncSession) -> RestaurantFoodLink:
    """
    Add a food item to a restaurant's menu (creates a RestaurantFoodLink).
    """
    new_item = RestaurantFoodLink(
        restaurant_id=restaurant_id,
        food_id=food_id,
        price=price
    )
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)

    return new_item


async def get_menu_item(restaurant_id: int, food_id, db: AsyncSession) -> Optional[RestaurantFoodLink]:
    """
    Check if a specific food item is already on a specific restaurant's menu.
    """
    query = select(RestaurantFoodLink).where(RestaurantFoodLink.restaurant_id == restaurant_id, RestaurantFoodLink.food_id == food_id)
    result = await db.execute(query)

    return result.scalars().one_or_none()


async def delete_menu_item(db_menu_item: RestaurantFoodLink, db: AsyncSession):
    await db.delete(db_menu_item)
    await db.commit()

    return 


#------ Order Crud ------

async def get_order_by_user(user_id: int, db: AsyncSession) -> List[Order]:
    query = select(Order).where(Order.user_id == user_id).order_by(Order.id.desc())
    result = await db.execute(query)
    return result.scalars().all()


async def get_order_by_id(order_id: int, db: AsyncSession) -> Order:
    query = select(Order).where(Order.id == order_id)
    result = await db.execute(query)
    return result.scalars().one_or_none()


# ------ Update Menu Item ------

async def update_menu_item(db_menu_item: RestaurantFoodLink, item_update: MenuLinkUpdate, db: AsyncSession) -> RestaurantFoodLink:
    update_data = item_update.model_dump(exclude_unset=True)
    db_menu_item.sqlmodel_update(update_data)

    db.add(db_menu_item)
    await db.commit()
    await db.refresh(db_menu_item)
    return db_menu_item