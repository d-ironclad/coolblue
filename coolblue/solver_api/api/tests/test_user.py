import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

client = APIClient()

user_kwargs = {
                "username": "test",
                "password": "test",
                "email": "test@test.com"
            }


@pytest.fixture
def user():
    user = User.objects.create_user(**user_kwargs)
    return user

class TestUserAPI:

    @pytest.mark.django_db
    def test_create_success(self):
        response = client.post(
            "/api/user/", user_kwargs, format="json"
        )
        assert response.status_code == 201, response.body
        assert response.json().get("id")
        assert response.json()['username'] == user_kwargs['username']

    @pytest.mark.django_db
    def test_create_fail(self, user):
        client.login(username="test", password="t")
        response = client.post(
            "/api/user/", user_kwargs, format="json"
        )
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_user_fail_auth(self, user):
        client.login(username="test", password="te")
        response = client.get("/api/user/1/", user=user)
        assert response.status_code == 403