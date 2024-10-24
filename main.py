import os
from city_walker.map_processor import load_map, get_total_streets, save_map, load_saved_map
from city_walker.gpx_handler import load_gpx, get_new_gpx_files, save_metadata, is_processed
from city_walker.street_matcher import build_spatial_index, match_streets, update_visited_streets
from city_walker.route_generator import generate_route, export_route
from city_walker.progress_tracker import load_visited_streets, save_visited_streets, calculate_percentage_visited

def main():
    # Parameters
    city_name = 'City of Edinburgh'
    map_file = 'map_data/city_map.graphml'
    gpx_dir = 'gpx_files'
    visited_streets_file = 'visited_streets.json'
    metadata_file = 'gpx_metadata.json'
    
    # Load or download map
    if os.path.exists(map_file):
        print(f"Loading saved map from {map_file}...")
        G = load_saved_map(map_file)
    else:
        print(f"Downloading map for {city_name}...")
        G = load_map(city_name)
        save_map(G, map_file)
        print(f"Map saved to {map_file}.")
    
    # Load visited streets
    visited_streets = load_visited_streets(visited_streets_file)
    total_streets = get_total_streets(G)
    print(f"Total streets in the city: {total_streets}")
    
    # Process new GPX files
    new_gpx_files = get_new_gpx_files(gpx_dir, metadata_file)
    if new_gpx_files:
        spatial_index = build_spatial_index(G)
        for gpx_file in new_gpx_files:
            print(f"Processing {gpx_file}...")
            gps_points = load_gpx(gpx_file)
            matched_streets = match_streets(gps_points, G, spatial_index)
            update_visited_streets(matched_streets, visited_streets)
            save_metadata(gpx_file, metadata_file)
        save_visited_streets(visited_streets, visited_streets_file)
    else:
        print("No new GPX files to process.")
    
    # Calculate progress
    percentage_visited = calculate_percentage_visited(visited_streets, total_streets)
    print(f"You have visited {percentage_visited:.2f}% of the city's streets.")
    
    # Generate a new route (example)
    start_point = (37.7749, -122.4194)  # Example coordinates, replace with your starting point
    print("Generating a new route...")
    route = generate_route(G, start_point, distance=5000)  # 5 km route
    export_route(G, route, 'new_route.gpx')
    print("New route exported to new_route.gpx.")

if __name__ == "__main__":
    main()

