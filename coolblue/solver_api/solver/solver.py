"""
    Simple Vehicles Routing Problem (VRP).
    Uses this Google OR-Tools tutorial:
    https://developers.google.com/optimization/routing/vrp
"""
import logging

from ortools.constraint_solver import pywrapcp, routing_enums_pb2

from solver_api.utils import calculate_distance

logger = logging.getLogger(__name__)


def create_distance_matrix(coordinates):
    """Creates distance matrix from list of coordinates"""
    data = []
    # TODO actual distance
    for point in coordinates:
        data.append([calculate_distance(point, x) for x in coordinates])
    logger.info(data)
    return data


def format_solution(solution, num_vehicles, routing, manager):
    """Returns solution as dict"""
    logger.info(f"Objective: {solution.ObjectiveValue()}")
    max_route_distance = 0
    for vehicle_id in range(num_vehicles):
        index = routing.Start(vehicle_id)
        plan_output = "Route for vehicle {}:\n".format(vehicle_id)
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += " {} -> ".format(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id
            )
        plan_output += "{}\n".format(manager.IndexToNode(index))
        plan_output += "Distance of the route: {}m\n".format(route_distance)
        logger.info(plan_output)
        max_route_distance = max(route_distance, max_route_distance)
    logger.info("Maximum of the route distances: {}m".format(max_route_distance))

    result = {"objective": solution.ObjectiveValue(), 'vehicles': {}}
    max_route_distance = 0
    for vehicle_id in range(num_vehicles):
        route = result['vehicles'].setdefault(vehicle_id, {"route": [], "distance": 0})
        index = routing.Start(vehicle_id)
        while not routing.IsEnd(index):
            route["route"].append(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route["distance"] += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id
            )
        route["route"].append(manager.IndexToNode(index))
    return result


def solve(
    distance_matrix: list, max_distance: int, num_vehicles: int = 1, depot: int = 0
):
    """Returns Vehicle Routing Problem solution"""
    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(distance_matrix), num_vehicles, depot)

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint.
    dimension_name = "Distance"
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        max_distance,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name,
    )
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    return format_solution(solution, num_vehicles, routing, manager)
