import gpxpy
import hashlib
import os
import json

def load_gpx(file_path):
    """
    Load and parse a GPX file to extract GPS points.
    
    Parameters:
        file_path (str): The path to the GPX file.
    
    Returns:
        List of tuples containing latitude and longitude ([(lat, lon), ...]).
    """
    with open(file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        gps_points = [(point.latitude, point.longitude) for track in gpx.tracks for segment in track.segments for point in segment.points]
    return gps_points

def get_gpx_hash(file_path):
    """
    Generate a hash of the GPX file for tracking purposes.
    
    Parameters:
        file_path (str): The path to the GPX file.
    
    Returns:
        str: A hash string of the GPX file.
    """
    with open(file_path, 'rb') as f:
        file_content = f.read()
        return hashlib.md5(file_content).hexdigest()

def is_processed(file_path, metadata_file):
    """
    Check if a GPX file has already been processed.
    
    Parameters:
        file_path (str): The path to the GPX file.
        metadata_file (str): Path to the metadata file.
    
    Returns:
        bool: True if the file has been processed, False otherwise.
    """
    gpx_hash = get_gpx_hash(file_path)
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
            return gpx_hash in metadata
    return False

def save_metadata(file_path, metadata_file):
    """
    Save the hash of the processed GPX file in the metadata file.
    
    Parameters:
        file_path (str): The path to the GPX file.
        metadata_file (str): Path to the metadata file.
    """
    gpx_hash = get_gpx_hash(file_path)
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
    else:
        metadata = {}
    
    metadata[gpx_hash] = True
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f)

def get_new_gpx_files(gpx_dir, metadata_file):
    """
    Get a list of GPX files that haven't been processed yet.
    
    Parameters:
        gpx_dir (str): Directory containing GPX files.
        metadata_file (str): Path to the metadata file.
    
    Returns:
        list: A list of new GPX files to process.
    """
    new_gpx_files = []
    for gpx_file in os.listdir(gpx_dir):
        file_path = os.path.join(gpx_dir, gpx_file)
        if not is_processed(file_path, metadata_file):
            new_gpx_files.append(file_path)
    return new_gpx_files

