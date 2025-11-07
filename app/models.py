from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


class RestaurantFoodLink(SQLModel, table=True):
    __tablename__ = "restaurant_food_links"

    restaurant_id: int = Field(foreign_key="restaurants.id", primary_key=True)
    food_id: int = Field(foreign_key="foods.id", primary_key=True)
    price: float
    food_rating: Optional[float] = Field(default=None)


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default= None, primary_key=True)
    name: str 
    email: str = Field(unique=True, index=True)
    hashed_password: str

    orders: List["Order"] = Relationship(back_populates="user")
    restaurants: List["Restaurant"] = Relationship(back_populates="owner", sa_relationship_kwargs={"lazy": "selectin"})


class Restaurant(SQLModel, table=True):
    __tablename__ = "restaurants"

    id: Optional[int] = Field(default= None, primary_key=True)
    name: str = Field(index=True, unique=True)
    rating: Optional[float] = Field(default= None)

    owner_id: int = Field(foreign_key="users.id")
    owner: "User" = Relationship(back_populates="restaurants", sa_relationship_kwargs={"lazy": "joined"})

    foods: List["Food"] = Relationship(back_populates="restaurants", link_model=RestaurantFoodLink)
    orders: List["Order"] = Relationship(back_populates="restaurant")


class Food(SQLModel, table=True):
    __tablename__ = "foods"

    id: Optional[int] = Field(default= None, primary_key=True)
    name: str
    description: Optional[str] = Field(default=None)

    restaurants: List["Restaurant"] = Relationship(back_populates="foods", link_model=RestaurantFoodLink)
    order_items: List["OrderItem"] = Relationship(back_populates="food")


class Order(SQLModel, table=True):
    __tablename__= "orders"

    id: Optional[int] = Field(default= None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    restaurant_id: int = Field(foreign_key="restaurants.id")
    total_price: float

    user : "User" = Relationship(back_populates="orders")
    restaurant: "Restaurant" = Relationship(back_populates="orders")
    items: List["OrderItem"] = Relationship(back_populates="order")


class OrderItem(SQLModel, table=True):
    __tablename__ = "order_items"

    id: Optional[int] = Field(default= None, primary_key=True)
    quantity: int
    price: float
    order_id: int = Field(foreign_key="orders.id")
    food_id: int = Field(foreign_key="foods.id")

    food : "Food" = Relationship(back_populates="order_items")
    order: "Order" = Relationship(back_populates="items")