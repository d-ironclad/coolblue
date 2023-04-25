"""Solver views"""
import logging
import uuid
from drf_spectacular.utils import extend_schema

from rest_framework import status
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from ...celery_app import app as celery_app
from ...solver.tasks import task_solve_problem


from .serializers import ProblemResponseSerializer, ProblemSerializer, SolutionSerializer

logger = logging.getLogger(__name__)

@extend_schema(request=ProblemSerializer, responses=ProblemResponseSerializer)
class SolverViewset(ViewSet):
    """Viewset for posting problem and receiving result"""

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        """Launches calculation task with given parameters, returns task id for retrieving"""
        serializer = ProblemSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            # user id added to task id to separate results
            task_id = str(uuid.uuid4())
            task_solve_problem.apply_async(
                kwargs={"user_id": request.user.id, "data": data}, queue="vrp_solver",
                task_id=":".join((str(request.user.id), task_id))
            )
            return Response(status=201, data={'task_id': task_id})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(responses=SolutionSerializer)
    def retrieve(self, request, pk=None):
        """Retrieves task result by id"""
        task_result = celery_app.AsyncResult(id=":".join((str(request.user.id), pk)))
        if task_result.ready():
            result = task_result.get()
            task_result.forget()
            return Response(result)
        return Response(status=400)
