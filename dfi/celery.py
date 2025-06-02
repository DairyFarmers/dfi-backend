import os
from celery import Celery
from celery.signals import after_setup_logger
import logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dfi.settings')

logger = logging.getLogger('celery')

app = Celery('dfi')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@after_setup_logger.connect
def setup_celery_logging(logger, *args, **kwargs):
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh = logging.FileHandler('logs/celery.log')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')