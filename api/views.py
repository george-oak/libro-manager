from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from books.models import Book, StockEvent
from books.tasks import restock_book
from django.utils import timezone
from datetime import timedelta
from .serializers import BookBuySerializer


class BookBuyView(APIView):
    def post(self, request, pk):
        book = Book.objects.filter(pk=pk).first()
        if not book:
            return Response(
                {"error": "Libro no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = BookBuySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        quantity = serializer.validated_data['quantity']

        if book.stock < quantity:
            return Response(
                {"error": "Stock insuficiente"},
                status=status.HTTP_400_BAD_REQUEST
            )

        book.stock -= quantity
        book.save()

        # eta = timezone.now() + timedelta(days=3)
        eta = timezone.now() + timedelta(seconds=10)
        event = StockEvent.objects.create(
            book=book,
            quantity=quantity,
            is_completed=False,
            scheduled_for=eta
        )
        restock_book.apply_async(
            args=[event.id],
            eta=eta
        )

        return Response({
            "success": f"Compra realizada. Stock actual: {book.stock}",
            "replenishment_date": eta.isoformat()
        }, status=status.HTTP_200_OK)
