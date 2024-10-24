import osmnx as ox
import networkx as nx

def load_map(place_name):
    """
    Load the map from OpenStreetMap for the specified place using osmnx.
    
    Parameters:
        place_name (str): Name of the place (e.g., city, neighborhood).
    
    Returns:
        G (networkx.MultiDiGraph): The street network of the place.
    """
    G = ox.graph_from_place(place_name, network_type='walk')
    return G

def get_total_streets(G):
    """
    Get the total number of unique streets in the graph.

    Parameters:
        G (networkx.MultiDiGraph): The street network graph.
    
    Returns:
        int: The total number of streets (edges) in the graph.
    """
    return len(G.edges)

def save_map(G, file_path):
    """
    Save the street network graph to a file.

    Parameters:
        G (networkx.MultiDiGraph): The street network graph.
        file_path (str): File path to save the graph.
    """
    ox.save_graphml(G, file_path)

def load_saved_map(file_path):
    """
    Load the street network graph from a saved file.
    
    Parameters:
        file_path (str): Path to the saved graph file.
    
    Returns:
        G (networkx.MultiDiGraph): The loaded street network graph.
    """
    return ox.load_graphml(file_path)

