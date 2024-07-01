"""
Celery is an asynchronous task queue/job queue based on distributed message passing.
It is used to execute tasks asynchronously outside the normal HTTP request-response cycle.
Celery helps manage and distribute tasks across worker processes or machines.
"""

from celery import Celery
import os
from PIL import Image
from utils.logger import create_logger

logging = create_logger(__name__)

celery = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)


@celery.task
def process_image(image_path, output_dir):
    try:
        img = Image.open(image_path)
        resized_img = img.resize((300, 300))
        output_path = os.path.join(output_dir, os.path.basename(image_path))
        resized_img.save(output_path)
        return output_path
    except Exception as e:
        logging.error(e)
