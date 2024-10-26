import osmnx as ox
import networkx as nx
from shapely.geometry import Point, LineString
from rtree import index

def build_spatial_index(G):
    """
    Build a spatial index for the edges in the graph, which helps with matching GPX points to streets.

    Parameters:
        G (networkx.MultiDiGraph): The street network graph.

    Returns:
        rtree.index.Index: A spatial index of the graph's edges.
    """
    idx = index.Index()

    for u, v, key, data in G.edges(keys=True, data=True):
        u_coord = (G.nodes[u]['x'], G.nodes[u]['y'])
        v_coord = (G.nodes[v]['x'], G.nodes[v]['y'])

        line = LineString([u_coord, v_coord])

        idx.insert(key, line.bounds, obj=(u, v, key))

    return idx

def match_streets(gps_points, G, spatial_index):
    """
    Match GPS points to the closest street segment in the city map.
    
    Parameters:
        gps_points (list): List of GPS points (latitude, longitude).
        G (networkx.MultiDiGraph): The street network graph.
        spatial_index (rtree.index.Index): The spatial index for the street segments.
    
    Returns:
        list: List of matched street segments.
    """
    matched_streets = set()
    for lat, lon in gps_points:
        point = Point(lon, lat)
        nearest_edges = list(spatial_index.nearest(point.bounds, 1, objects=True))
        for edge in nearest_edges:
            u, v, _ = edge.object
            matched_streets.add((u, v))
    return matched_streets

def update_visited_streets(matched_streets, visited_streets):
    """
    Update the visited streets set with new matched streets.
    
    Parameters:
        matched_streets (list): List of newly matched street segments.
        visited_streets (set): Set of previously visited streets.
    """
    visited_streets.update(matched_streets)

