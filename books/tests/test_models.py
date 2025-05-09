from django.db import IntegrityError
from books.models import Book
import pytest
from django.core.exceptions import ValidationError

@pytest.mark.django_db
def test_book_stock_negative():
    with pytest.raises(ValidationError):
        book = Book(title="Libro Inválido", stock=-5, price=10)
        book.full_clean()

@pytest.mark.django_db
def test_book_price_positive():
    with pytest.raises(ValidationError):
        book = Book(title="Libro Gratis", stock=10, price=0)
        book.full_clean()

@pytest.mark.django_db
def test_book_title_required():
    with pytest.raises(IntegrityError):
        Book.objects.create(title=None, stock=10, price=20)
