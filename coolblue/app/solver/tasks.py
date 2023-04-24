from . import solver
from coolblue.app import celery_app


@celery_app.task(bind=True)
def task_solve_problen(self, user_id, data):

    distance_matrix = solver.create_distance_matrix(data['coordinates'])
    solution = solver.solve(
                distance_matrix=distance_matrix,
                num_vehicles=data['num_vehicles'],
                depot=data['depot'],
                max_distance=data['max_distance'],
                )
    return {'result': 'result'}
