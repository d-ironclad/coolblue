'''API urls'''

from rest_framework import routers

from .views import SolveViewset

router = routers.SimpleRouter()

router.register(r'solve', SolveViewset, basename='solver')
