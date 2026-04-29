import time
from app.core.celery_app import celery


@celery.task(name="notify_restaurant_new_food")
def notify_restaurant(order_id: int, restaurant_id: int, total_price: float):
    # Simulate a delay (e.g., for sending an email or processing the order)

    # Here you would implement the actual notification logic, such as sending an email
    print(f"Notification: New order {order_id} for restaurant {restaurant_id}")
    
    time.sleep(5)

    print(f"Total price: ${total_price:.2f}")

    return True