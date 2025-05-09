import pytest
from django.utils import timezone
from books.models import StockEvent
from books.tasks import restock_book

@pytest.mark.django_db
@pytest.mark.celery
def test_restock_book_task(sample_book):
    initial_stock = sample_book.stock
    reposition_quantity = 3

    event = StockEvent.objects.create(
        book=sample_book,
        quantity=reposition_quantity,
        is_completed=False,
        scheduled_for=timezone.now()
    )

    restock_book.delay = lambda *args, **kwargs: restock_book(*args, **kwargs)
    restock_book(event.id)

    event.refresh_from_db()
    sample_book.refresh_from_db()
    assert event.is_completed is True
    assert sample_book.stock == initial_stock + reposition_quantity
