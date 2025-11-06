from sqlmodel import SQLModel, Field
from typing import List, Annotated, Optional
from pydantic import EmailStr


class UserCreate(SQLModel):
    name: Annotated[str, Field(min_length=2, max_length=30)]
    email: EmailStr
    password: Annotated[str, Field(min_length=4)]


class UserRead(SQLModel):
    id: int
    name: str
    email: EmailStr


class RestaurantBase(SQLModel):
    name: str
    rating: Optional[float] = None


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantRead(RestaurantBase):
    id: int


class FoodBase(SQLModel):
    name: str
    description: Optional[str] = None


class FoodCreate(FoodBase):
    pass


class FoodRead(FoodBase):
    id: int


class OrderItemCreate(SQLModel):
    food_id: int
    quantity: int


class OrderItemRead(SQLModel):
    id: int
    food: FoodRead
    quantity: int
    price: float


class OrderCreate(SQLModel):
    restaurant_id: int
    order_items: List[OrderItemCreate]
    

class OrderRead(SQLModel):
    id: int
    user: UserRead
    restaurant: RestaurantRead
    order_items: List[OrderItemRead]
    total_price: float


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    email: Optional[str] = None