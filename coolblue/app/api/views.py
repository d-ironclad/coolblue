import logging

from celery.result import AsyncResult
from coolblue.app import celery_app

from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response


from .serializers import ProblemSerialiser
from ..solver.tasks import task_solve_problen
logger = logging.getLogger(__name__)


class SolveViewset(ViewSet):
    def create(self, request):
        serializer = ProblemSerialiser(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            result = task_solve_problen.apply_async(
                kwargs={'user_id': request.user.id, 'data': data}, queue='vrp_solver'
                )
            return Response(result.id)
        else:
            return Response(serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):

        res = AsyncResult(id='432890aa-4f02-437d-aaca-1999b70efe8d', app=celery_app)
        print(res.state)


        if not res.failed():
            return Response(res.collect())
        return Response(status=400)


