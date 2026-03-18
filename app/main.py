from fastapi import FastAPI
from .routers import auth, users, restaurants, foods, orders
from sqlmodel import SQLModel
from contextlib import asynccontextmanager
from . import models


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application starting up")
    yield
    print("application shutting down")


app = FastAPI(
    title="Food Delivery App",
    description="This is the api for food delivery app.",
    version="1.0",
    lifespan=lifespan
)


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(restaurants.router)
app.include_router(foods.router)
app.include_router(orders.router)


@app.get("/")
async def root():
    return {"msg" : "Welcome to the Food Delivery Api"}