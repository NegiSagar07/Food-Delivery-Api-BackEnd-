from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..dependencies import get_current_user
from ..database import get_db
from ..schemas import OrderCreate, OrderRead
from ..models import User, OrderItem, Order
from ..crud import get_restaurant_by_id, get_menu_item, get_order_by_user, get_order_by_id
from typing import List


router = APIRouter(prefix="/order", tags=["Order"])


@router.post("/", response_model=OrderRead)
async def create_new_order(order_in: OrderCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    restaurant = await get_restaurant_by_id(id=order_in.restaurant_id, db=db)
    if not restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="restaurant not found")
    
    total_price = 0.0
    order_items = []

    for item in order_in.items:
        menu_item = await get_menu_item(
            restaurant_id=order_in.restaurant_id,
            food_id=item.food_id,
            db=db
        )
        if not menu_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"food item with {item.food_id} not found in this restaurant")
        
        item_price = menu_item.price * item.quantity
        total_price += item_price

        db_item = OrderItem(
            food_id=item.food_id,
            quantity=item.quantity,
            price=menu_item.price
        )

        order_items.append(db_item)
    
    db_order = Order(
        user_id=current_user.id,
        restaurant_id=order_in.restaurant_id,
        total_price=total_price,
        items=order_items
    )

    try:
        db.add(db_order)
        await db.commit()
        await db.refresh(db_order)

        return db_order
        
    except Exception as e:
        # If anything fails, roll back
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the order: {e}"
        )
    

@router.get("/", response_model=List[OrderRead])
async def get_my_orders(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    orders = await get_order_by_user(user_id=current_user.id, db=db)

    if not orders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="you didn't have placed any order yet")
    
    return orders


@router.get("/{order_id}", response_model=OrderRead)
async def get_sepecif_order(order_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):

    order = await get_order_by_id(order_id= order_id, db=db)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order not found")
    
    if order.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you are not authorized to view this order")
    
    return order