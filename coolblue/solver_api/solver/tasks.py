""" Celery tasks """
from solver_api import celery_app

from . import solver


@celery_app.task(bind=True)
def task_solve_problem(self, user_id, data):
    """Task for calculating distance problem and VRP solution"""
    distance_matrix = solver.create_distance_matrix(data["coordinates"])
    solution = solver.solve(
        distance_matrix=distance_matrix,
        num_vehicles=data["num_vehicles"],
        depot=data["depot"],
        max_distance=data["max_distance"],
    )
    return {"result": "result"}
