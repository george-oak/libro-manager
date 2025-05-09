import os
import pytest
import django
from django.conf import settings
from celery.contrib.testing import worker


def pytest_configure():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'libro_manager.settings')
    django.setup()

@pytest.fixture(autouse=True)
def celery_config():
    return {
        "task_always_eager": True,
        "broker_url": "memory://",
    }

@pytest.fixture(scope='session')
def celery_worker(celery_config):
    with worker.start_worker(**celery_config) as w:
        yield w
