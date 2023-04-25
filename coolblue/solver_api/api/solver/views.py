import logging

from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from coolblue.solver_api import celery_app


from coolblue.solver_api.solver.tasks import task_solve_problem
from .serializers import ProblemSerialiser

logger = logging.getLogger(__name__)


class SolverViewset(ViewSet):
    """Viewset for posting problem and receiving result"""

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        """Launces calculation task with given parameters, returns task id for retrieving"""
        serializer = ProblemSerialiser(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            result = task_solve_problem.apply_async(
                kwargs={"user_id": request.user.id, "data": data}, queue="vrp_solver"
            )
            return Response(result.id)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Retrieves task result by id"""
        task_result = celery_app.AsyncResult(id=pk)
        if task_result.ready():
            result = task_result.get()
            return Response(result)
        return Response(status=400)
