import logging

from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from vrp import solver



from .serializers import ProblemSerialiser

logger = logging.getLogger(__name__)


class SolveViewset(ViewSet):
    def create(self, request):
        serializer = ProblemSerialiser(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            distance_matrix = solver.create_data_model(data['coordinates'])
            solution = solver.solve(
                distance_matrix=distance_matrix,
                num_vehicles=data['num_vehicles'],
                depot=data['depot'],
                max_distance=data['max_distance']
                )
            print(solution)
            return Response(data=solution)

        else:
            return Response(serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)



