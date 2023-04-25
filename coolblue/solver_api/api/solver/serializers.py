from rest_framework import serializers


class Coordinates(serializers.Serializer):
    """Waypoint serializer"""
    lat = serializers.FloatField(min_value=-90, max_value=90)
    lon = serializers.FloatField(min_value=-180, max_value=180)


class ProblemSerialiser(serializers.Serializer):
    """Problem input serializer"""
    coordinates = Coordinates(many=True)
    num_vehicles = serializers.IntegerField(min_value=1)
    depot = serializers.IntegerField(min_value=0)
    max_distance = serializers.IntegerField()

class RouteSerializer(serializers.Serializer):
    """Route of one vehicle"""
    route = serializers.ListField(child=serializers.IntegerField())
    distance = serializers.FloatField()

class SolutionSerializer(serializers.Serializer):
    objective = serializers.FloatField
    vehicles = serializers.DictField(child=RouteSerializer())