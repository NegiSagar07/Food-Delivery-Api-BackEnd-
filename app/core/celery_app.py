from celery import Celery
from .config import settings

celery = Celery(
    "food_delivery_app",
    broker = settings.REDIS_URL,
    backend = settings.REDIS_URL,
    include = ["app.tasks.restaurant", "app.tasks.email_tasks"]
)