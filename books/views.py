from datetime import timedelta
from .models import Book, StockEvent
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import (
    View,
    ListView,
    UpdateView,
    DeleteView,
    CreateView
)
from .tasks import restock_book


class BookListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Book
    template_name = 'books/list.html'
    context_object_name = 'books'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stock_events'] = StockEvent.objects.all() \
            .order_by('-scheduled_for') \
            .distinct('book', 'scheduled_for')
        return context


class BookCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Book
    fields = ['title', 'price', 'stock']
    template_name = 'books/form.html'
    success_url = reverse_lazy('book-list')


class BookUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = Book
    fields = ['title', 'price', 'stock']
    template_name = 'books/form.html'
    success_url = reverse_lazy('book-list')


class BookDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    model = Book
    template_name = 'books/confirm_delete.html'
    success_url = reverse_lazy('book-list')


class BuyStockView(LoginRequiredMixin, View):
    login_url = '/login/'
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        quantity = int(request.POST.get('quantity', 0))

        if quantity <= 0:
            messages.error(request, "La cantidad debe ser mayor a cero")
            return redirect('book-list')

        eta = timezone.now() + timedelta(days=3)
        event = StockEvent.objects.create(
            book=book,
            quantity=quantity,
            is_completed=False,
            scheduled_for=eta
        )

        restock_book.apply_async(
            args=[event.id],
            eta=event.scheduled_for
        )

        messages.success(request, f"¡Reposición programada para {eta.strftime('%d/%m/%Y')}!")
        return redirect('book-list')


def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('book-list')
    return render(request, 'registration/login.html')


def custom_logout(request):
    logout(request)
    return redirect('login')
