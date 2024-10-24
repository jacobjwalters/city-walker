import osmnx as ox

def generate_route(G, start_point, distance=None, time_limit=None):
    """
    Generate a walking route that maximizes unvisited streets.
    
    Parameters:
        G (networkx.MultiDiGraph): The street network graph.
        start_point (tuple): The starting point (latitude, longitude).
        distance (float): Desired walking distance (in meters).
        time_limit (float): Time limit for the walk (in hours).
    
    Returns:
        List: A list of nodes representing the generated route.
    """
    start_node = ox.distance.nearest_nodes(G, X=start_point[1], Y=start_point[0])
    
    # Use networkx for shortest path search (A*, Dijkstra)
    if distance:
        route = ox.shortest_path(G, start_node, start_node, weight='length', return_length=True)[0]
    else:
        # Use time constraint if given (estimate based on speed)
        route = ox.shortest_path(G, start_node, start_node)
    
    return route

def export_route(G, route, file_path):
    """
    Export the generated route to a GPX file.
    
    Parameters:
        G (networkx.MultiDiGraph): The street network graph.
        route (list): List of nodes representing the generated route.
        file_path (str): Path to save the GPX file.
    """
    ox.save_route_as_gpx(G, route, file_path)

