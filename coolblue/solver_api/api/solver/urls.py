"""API urls"""

from rest_framework import routers

from .views import SolverViewset

router = routers.SimpleRouter()

router.register(r"solve", SolverViewset, basename="solver")
