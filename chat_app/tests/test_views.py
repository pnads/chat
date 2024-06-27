import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def test_user(db):
    return User.objects.create_user(username="testuser", password="12345")


def test_room_view(client, test_user):
    client.force_login(test_user)
    response = client.get(reverse("chat:room", args=["room1"]))
    assert response.status_code == 200


def test_send_message_view(client, test_user):
    client.force_login(test_user)
    room_name = "room1"
    response = client.post(
        reverse("chat:send_message", args=[room_name]),
        {"message": "Test message", "room": room_name},
        content_type="application/json",
    )
    assert response.status_code == 200


def test_fetch_messages_view(client, test_user):
    client.force_login(test_user)
    room_name = "room1"
    response = client.get(reverse("chat:fetch_messages", args=[room_name]))
    assert response.status_code == 200
