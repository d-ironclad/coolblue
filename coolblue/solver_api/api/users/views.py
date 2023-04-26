"""User viewsets"""
from django.contrib.auth import get_user_model
from rest_framework import mixins
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from .serializers import UserSerializer


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    """CRUD viewset for User"""

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = get_user_model().objects
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (AllowAny,)
            self.authentication_classes = []

        return super(UserViewSet, self).get_permissions()
