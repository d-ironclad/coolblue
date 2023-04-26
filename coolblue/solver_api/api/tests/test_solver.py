import logging

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

client = APIClient()

logger = logging.getLogger(__name__)


@pytest.fixture
def user():
    user = User.objects.create_user("test", "test@test.com", "test")
    return user


@pytest.fixture
def problem():
    return {
        "coordinates": [
            {"lat": 456, "lon": 320},
            {"lat": 228, "lon": 0},
            {"lat": 912, "lon": 0},
        ],
        "num_vehicles": 4,
        "depot": 0,
        "max_distance": 3000,
    }


class TestSolveAPI:
    @pytest.mark.django_db
    def test_solve_success(self, problem, user):
        """test succesful retrieving of task id"""
        client.login(username="test", password="test")
        response = client.post("/api/solve/", problem, format="json", user=user)
        task_id = response.json().get("task_id")

        assert response.status_code == 201, response.body
        assert task_id

    @pytest.mark.django_db
    def test_solve_fail_auth(self, problem):
        """test auth fail when posting task"""
        client.login(username="test", password="t")
        response = client.post("/api/solve/", problem, format="json", user=user)
        assert response.status_code == 403, response.body

    @pytest.mark.django_db
    def test_solve_fail_validation(self, problem, user):
        """test validation fail when posting task"""
        client.login(username="test", password="test")
        problem["num_vehicles"] = 0
        problem["coordinates"][0].pop("lat")
        response = client.post("/api/solve/", problem, format="json", user=user)
        assert response.status_code == 400, response.json()
