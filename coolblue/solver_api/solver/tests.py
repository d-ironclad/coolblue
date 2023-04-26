import pytest

from . import solver

@pytest.fixture
def problem():
    return {
        "coordinates": [
            {"lat": 456, "lon": 320},
            {"lat": 228, "lon": 0},
            {"lat": 912, "lon": 0},
            {"lat": 0, "lon": 80},
            {"lat": 114, "lon": 80},
            {"lat": 570, "lon": 160},
            {"lat": 798, "lon": 160},
            {"lat": 342, "lon": 240},
            {"lat": 684, "lon": 240},
            {"lat": 570, "lon": 400},
            {"lat": 912, "lon": 400},
            {"lat": 114, "lon": 480},
            {"lat": 228, "lon": 480},
            {"lat": 342, "lon": 560},
            {"lat": 684, "lon": 560},
            {"lat": 0, "lon": 640},
            {"lat": 798, "lon": 640},
        ],
        "num_vehicles": 4,
        "depot": 0,
        "max_distance": 3000,
    }

class TestSolver:
    def test_solver_success(self, problem):
        distance_matrix = solver.create_distance_matrix(problem["coordinates"])
        solution = solver.solve(
        distance_matrix=distance_matrix,
        num_vehicles=problem["num_vehicles"],
        depot=problem["depot"],
        max_distance=problem["max_distance"],
    )
        assert solution["objective"] == 125115
        assert solution["vehicles"][0]["route"] == [0,10,16,14,9,0]

    def test_solver_fail(self, problem):
        problem['max_distance'] = 10
        distance_matrix = solver.create_distance_matrix(problem["coordinates"])
        solution = solver.solve(
        distance_matrix=distance_matrix,
        num_vehicles=problem["num_vehicles"],
        depot=problem["depot"],
        max_distance=problem["max_distance"],
    )
        assert solution["objective"] == "Solution not found"

