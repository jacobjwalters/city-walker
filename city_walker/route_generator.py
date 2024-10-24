import osmnx as ox
import networkx as nx
import random
import gpxpy.gpx

def generate_route(G, start_point, visited_edges, distance):
    """
    Generate a route that prioritizes unvisited streets and fits within a specified distance.

    Parameters:
        G (networkx.MultiDiGraph): The street network graph.
        start_point (tuple): The starting point (latitude, longitude).
        visited_edges (set): A set of edges (street segments) that have already been visited.
        distance (float): Desired route distance (in meters).

    Returns:
        list: A list of nodes representing the generated route.
    """
    start_node = ox.distance.nearest_nodes(G, X=start_point[1], Y=start_point[0])

    # Initialize variables
    current_node = start_node
    route = [current_node]
    total_distance = 0
    visited_in_route = set()  # Track visited edges during this route

    while total_distance < distance:
        neighbors = list(G.neighbors(current_node))
        random.shuffle(neighbors)  # Shuffle to avoid bias

        next_node = None
        best_edge = None

        for neighbor in neighbors:
            edge_data = G.get_edge_data(current_node, neighbor, 0)
            edge_length = edge_data['length']

            # Check if the edge has already been visited (in this route or globally)
            edge_key = (current_node, neighbor, 0)
            if edge_key in visited_edges or edge_key in visited_in_route:
                continue  # Skip already visited edges

            # Avoid going over the distance limit
            if total_distance + edge_length > distance:
                continue

            # Select this edge as the best option
            next_node = neighbor
            best_edge = edge_key
            break

        # If no unvisited edge is found, allow revisiting an edge as a last resort
        if not next_node:
            for neighbor in neighbors:
                edge_data = G.get_edge_data(current_node, neighbor, 0)
                edge_length = edge_data['length']
                if total_distance + edge_length <= distance:
                    next_node = neighbor
                    best_edge = (current_node, neighbor, 0)
                    break

        if next_node:
            # Add the edge to the route and update total distance
            route.append(next_node)
            total_distance += G.get_edge_data(current_node, next_node, 0)['length']

            # Mark the edge as visited (both globally and in this route)
            visited_in_route.add(best_edge)
            visited_edges.add(best_edge)

            # Move to the next node
            current_node = next_node
        else:
            # No valid next node, end the route
            break

    return route

def export_route(G, route, file_path):
    """
    Export the generated route to a GPX file.
    
    Parameters:
        G (networkx.MultiDiGraph): The street network graph.
        route (list): List of nodes representing the generated route.
        file_path (str): Path to save the GPX file.
    """
    gpx = gpxpy.gpx.GPX()

    # Create a new GPX track
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)

    # Create a new GPX segment
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)

    # Add points (nodes) to the GPX segment
    for node in route:
        lat = G.nodes[node]['y']
        lon = G.nodes[node]['x']
        gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(lat, lon))

    # Save the GPX to a file
    with open(file_path, 'w') as f:
        f.write(gpx.to_xml())

