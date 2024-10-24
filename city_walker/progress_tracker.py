import json

def load_visited_streets(file_path):
    """
    Load the visited streets set from a JSON file.
    
    Parameters:
        file_path (str): Path to the JSON file.
    
    Returns:
        set: A set of visited streets.
    """
    try:
        with open(file_path, 'r') as f:
            visited_streets = set(tuple(street) for street in json.load(f))
    except FileNotFoundError:
        visited_streets = set()
    return visited_streets

def save_visited_streets(visited_streets, file_path):
    """
    Save the visited streets set to a JSON file.
    
    Parameters:
        visited_streets (set): A set of visited streets.
        file_path (str): Path to the JSON file.
    """
    with open(file_path, 'w') as f:
        json.dump(list(visited_streets), f)

def calculate_percentage_visited(visited_streets, total_streets):
    """
    Calculate the percentage of the city streets visited.
    
    Parameters:
        visited_streets (set): A set of visited streets.
        total_streets (int): The total number of streets in the city.
    
    Returns:
        float: The percentage of streets visited.
    """
    if total_streets == 0:
        return 0.0
    return (len(visited_streets) / total_streets) * 100

