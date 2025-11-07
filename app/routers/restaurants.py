from fastapi import APIRouter, status, Depends, HTTPException
from ..schemas import RestaurantRead, RestaurantCreate
from sqlalchemy.ext.asyncio import AsyncSession
from ..dependencies import get_current_user
from ..models import User
from ..database import get_db
from ..crud import get_restaurant_by_name, create_restaurant


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