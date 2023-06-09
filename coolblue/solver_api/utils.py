import math


def calculate_distance(point1, point2):
    """Returns Eucledian distance"""
    return int(
        math.dist((point1["lat"], point1["lon"]), (point2["lat"], point2["lon"]))
    )
