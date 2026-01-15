import sys
import os
from dotenv import load_dotenv
from graph_builder import GraphBuilder
from dijkstra import dijkstra

# Load environment variables
load_dotenv()

def format_time(seconds):
    """Helper to format seconds into readable hours/minutes."""
    if seconds < 60:
        return "< 1 min"
    minutes = int(seconds // 60)
    hours = minutes // 60
    minutes = minutes % 60
    if hours > 0:
        return f"{hours} hr {minutes} min"
    return f"{minutes} min"

def main():
    print("=========================================")
    print("      UBER-STYLE ROUTING SYSTEM          ")
    print("=========================================")
    
    # 1. Setup API Key from .env
    api_key = os.getenv("ORS_API_KEY")
    
    if not api_key:
        print("[Warning] 'ORS_API_KEY' not found in .env file.")
        print("Running in MOCK MODE.")
    else:
        print("[System] API Key loaded successfully.")
    
    # 2. Build the Graph
    print("\n[System] Constructing the City Map...")
    builder = GraphBuilder(api_key if api_key else None)
    graph, city_coords = builder.build_demo_graph()
    
    print("\n[System] Available Locations:")
    locations = sorted(list(builder.nodes))
    for i, loc in enumerate(locations):
        print(f" {i+1}. {loc}")
        
    # 3. User Inputs
    print("\n--- Route Selection ---")
    
    while True:
        try:
            start_idx = int(input(f"Select Start Location (1-{len(locations)}): ")) - 1
            if 0 <= start_idx < len(locations):
                source = locations[start_idx]
                break
            print(f"[Error] Please pick a number between 1 and {len(locations)}.")
        except ValueError:
            print("[Error] Invalid input. Please enter a NUMBER.")

    while True:
        try:
            end_idx = int(input(f"Select Destination (1-{len(locations)}): ")) - 1
            if 0 <= end_idx < len(locations):
                destination = locations[end_idx]
                break
            print(f"[Error] Please pick a number between 1 and {len(locations)}.")
        except ValueError:
            print("[Error] Invalid input. Please enter a NUMBER.")

    while True:
        try:
            speed_kmh = float(input("Enter Average Speed (km/h): "))
            if speed_kmh > 0:
                break
            print("[Error] Speed must be greater than 0.")
        except ValueError:
            print("[Error] Invalid input. Please enter a NUMBER/Decimal.")

    print(f"\n[Computing] Calculating best route from '{source}' to '{destination}'...")

    # 4. Run Algorithm
    shortest_dist_meters, path = dijkstra(graph, source, destination)

    if shortest_dist_meters == float('inf'):
        print(f"\n[Result] No path found between {source} and {destination}.")
    else:
        # 5. Calculate ETA
        # Distance is in meters. Speed is km/h.
        distance_km = shortest_dist_meters / 1000.0
        speed_mps = speed_kmh * (1000.0 / 3600.0) # Convert km/h to m/s
        travel_time_seconds = shortest_dist_meters / speed_mps
        
        print("\n=========================================")
        print("           RIDE DETAILS                  ")
        print("=========================================")
        print(f"🚖 Route: {' -> '.join(path)}")
        print(f"📏 Total Distance: {distance_km:.2f} km")
        print(f"⏱️  Estimated Time: {format_time(travel_time_seconds)}")
        print("=========================================")

if __name__ == "__main__":
    main()
