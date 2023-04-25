"""User viewsets"""
from django.contrib.auth import get_user_model
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny

from .serializers import UserSerializer


class UserViewSet(mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  GenericViewSet):
    """CRUD viewset for User"""
    queryset = get_user_model().objects
    serializer_class = UserSerializer


    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (AllowAny,)

        return super(UserViewSet, self).get_permissions()
