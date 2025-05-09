from django.urls import path
from .views import (
    BookListView,
    BookUpdateView,
    BookDeleteView,
    BookCreateView,
    BuyStockView,
)
from . import views

urlpatterns = [
    path('', BookListView.as_view(), name='book-list'),
    path('create/', BookCreateView.as_view(), name='book-create'),
    path('<int:pk>/edit/', BookUpdateView.as_view(), name='book-edit'),
    path('<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
    path(
        'books/<int:pk>/buy-stock/',
        BuyStockView.as_view(),
        name='buy-stock'
    ),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
]
