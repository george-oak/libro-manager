from celery import shared_task
from django.utils import timezone
from .models import StockEvent


@shared_task(bind=True)
def restock_book(self, event_id):
    try:
        event = StockEvent.objects.get(pk=event_id)
        book = event.book
        book.stock += event.quantity
        book.save()

        event.is_completed = True
        event.scheduled_for = timezone.now()
        event.save()

        return True
    except Exception as e:
        raise self.retry(exc=e, countdown=60)
