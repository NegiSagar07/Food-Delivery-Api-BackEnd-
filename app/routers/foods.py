from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas import FoodCreate, FoodRead
from ..database import get_db
from ..models import User
from ..dependencies import get_current_user
from ..crud import get_food_by_name, creat_food

router = APIRouter(prefix="/foods", tags=["Foods"])


@router.post("/", response_model=FoodRead)
async def create_new_food(food_in: FoodCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):

    db_food = await get_food_by_name(name=food_in.name, db=db)
    if db_food:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A Food item with this name already exist")
    
    new_food = await creat_food(name=food_in.name, description=food_in.description, db=db)

    return new_food