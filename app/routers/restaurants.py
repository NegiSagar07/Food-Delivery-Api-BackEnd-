from fastapi import APIRouter, status, Depends, HTTPException
from ..schemas import RestaurantRead, RestaurantCreate, MenuLinkCreate, MenuLinkRead
from sqlalchemy.ext.asyncio import AsyncSession
from ..dependencies import get_current_user
from ..models import User   
from ..database import get_db
from typing import List
from ..crud import get_restaurant_by_name, create_restaurant, get_restaurant_by_id, get_food_by_id, get_menu_item, add_item_to_menu, get_restaurant, get_restaurant_menu


router = APIRouter(prefix="/restaurant", tags=["Restaurant"])


@router.post("/", response_model=RestaurantRead, status_code=status.HTTP_201_CREATED)
async def create_new_restaurant(restaurant: RestaurantCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):

    db_restaurant = await get_restaurant_by_name(restaurant.name, db)
    if db_restaurant:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Restaurant name already exist")
    
    new_restaurant = await create_restaurant(
        name = restaurant.name,
        rating = restaurant.rating,
        owner_id = current_user.id,
        db = db
    )

    return new_restaurant


@router.post("/{restaurant_id}/menu", response_model=MenuLinkRead)
async def add_menu_item_to_restaurant(restaurant_id: int, menu_item: MenuLinkCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    restaurant = await get_restaurant_by_id(restaurant_id, db)
    if not restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
    
    if restaurant.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No authorize to add item to this restaurant's menu")
    
    food = await get_food_by_id(menu_item.food_id, db)
    if not food:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="food item not found")
    
    existing_item = await get_menu_item(restaurant_id=restaurant_id, food_id=menu_item.food_id, db=db)
    if existing_item:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This item is already in meny")
    
    new_menu_item = await add_item_to_menu(
        restaurant_id=restaurant_id,
        food_id=menu_item.food_id,
        price=menu_item.price,
        db=db
    )

    return new_menu_item


@router.get("/", response_model=List[RestaurantRead])
async def get_all_restaurant(skip: int = 0, limit:int = 100, db: AsyncSession = Depends(get_db)):
    restaurants = await get_restaurant(db=db, skip=skip, limit=limit)
    if not restaurants:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no restaurant available")
    
    return restaurants


@router.get("/{restaurant_id}/menu", response_model=List[MenuLinkRead])
async def get_menu_of_restaurant(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    
    restaurant = await get_restaurant_by_id(id=restaurant_id, db=db)
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found."
        )
    
    menu = await get_restaurant_menu(restaurant_id=restaurant_id, db=db)
    if not menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu is not found for this restaurant")
    
    return menu


