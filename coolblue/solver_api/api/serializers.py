from rest_framework import serializers


class Coordinates(serializers.Serializer):
    lat = serializers.FloatField(min_value=-90, max_value=90)
    lon = serializers.FloatField(min_value=-180, max_value=189)


class ProblemSerialiser(serializers.Serializer):
    coordinates = Coordinates(many=True)
    num_vehicles = serializers.IntegerField(min_value=1)
    depot = serializers.IntegerField(min_value=0)
    max_distance = serializers.IntegerField()
