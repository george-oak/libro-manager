from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.core.validators import MinValueValidator


class Book(models.Model):
    title = models.CharField(max_length=100)
    stock = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )


class StockEvent(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    scheduled_for = models.DateTimeField(
        default=timezone.now() + timedelta(days=3)
        )

    class Meta:
        ordering = ['-created_at']
        unique_together = ['book', 'scheduled_for']
