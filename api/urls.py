from django.urls import path
from .views import BookBuyView

urlpatterns = [
    path('book/buy/<int:pk>/', BookBuyView.as_view(), name='api-buy-book'),
]
