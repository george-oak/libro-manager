from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from books.models import Book


class BookBuyTests(APITestCase):

    quantity = 10

    def setUp(self):
        self.book = Book.objects.create(
            title="D&D PHB", stock=self.quantity, price=49.99
        )

    def test_buy_book_sufficient_stock(self):
        to_buy = 1
        url = reverse("api-buy-book", args=[self.book.id])
        data = {"quantity": to_buy}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.stock, self.quantity - to_buy)

    def test_buy_book_insufficient_stock(self):
        url = reverse("api-buy-book", args=[self.book.id])
        data = {"quantity": self.quantity + 1}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Stock insuficiente", str(response.data))
