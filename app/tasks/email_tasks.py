import time
from app.core.celery_app import celery

@celery.task(name="send_order_confirmation_email")
def send_welcome_email(user_email: str, user_name: str):
    # Dedicated task to send a welcome email to the user
    print(f"Sending welcome email to {user_email} for user {user_name}")
    time.sleep(3)  # Simulate email sending delay
    print(f"Welcome email sent to {user_email}")

    return True