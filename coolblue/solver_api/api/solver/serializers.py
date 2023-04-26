"""Serializers for problem and solution"""
from rest_framework import serializers


class Coordinates(serializers.Serializer):
    """Waypoint serializer"""

    lat = serializers.IntegerField()
    lon = serializers.IntegerField()


class ProblemSerializer(serializers.Serializer):
    """Problem input serializer"""

    coordinates = Coordinates(many=True)
    num_vehicles = serializers.IntegerField(min_value=1)
    depot = serializers.IntegerField(min_value=0)
    max_distance = serializers.IntegerField()


class ProblemResponseSerializer(serializers.Serializer):
    task_id = serializers.CharField()


class RouteSerializer(serializers.Serializer):
    """Route of one vehicle"""

    route = serializers.ListField(child=serializers.IntegerField())
    distance = serializers.FloatField()


class SolutionSerializer(serializers.Serializer):
    """Solution representation"""

    objective = serializers.FloatField
    vehicles = serializers.DictField(child=RouteSerializer())
