import pytest
from books.models import Book


@pytest.fixture
def sample_book(db):
    return Book.objects.create(
            title="D&D PHB", stock=10, price=49.99
        )
