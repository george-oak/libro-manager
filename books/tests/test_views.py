import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client

@pytest.mark.django_db
def test_worker_add_stock(sample_book):
    client = Client()
    worker_user = User.objects.create_user(
        username="worker",
        password="test",
        is_staff=True
    )
    client.force_login(worker_user)

    response = client.post(
        reverse("buy-stock", args=[sample_book.id]),
        {"quantity": 3},
        follow=True
    )

    assert response.status_code == 200
    messages = list(response.context['messages'])
    assert len(messages) == 1
    assert "Reposición programada" in str(messages[0])
