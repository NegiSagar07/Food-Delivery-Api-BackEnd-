from fastapi import APIRouter, Depends
from ..schemas import UserRead
from ..dependencies import get_current_user
from ..models import User


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=UserRead)
async def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user
