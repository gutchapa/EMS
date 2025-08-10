
from celery import Celery
import os

REDIS_URL = os.environ.get("REDIS_URL", "redis://redis:6379/0")
celery_app = Celery("ems_worker", broker=REDIS_URL, backend=REDIS_URL)
