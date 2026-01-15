import requests
import time

def get_coordinates(api_key, place_name):
    """
    Fetches the (longitude, latitude) for a place name using 
    OpenRouteService Geocoding API.
    """
    base_url = "https://api.openrouteservice.org/geocode/search"
    params = {
        "api_key": api_key,
        "text": place_name,
        "size": 1  # We only want the top result
    }
    
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        
        if response.status_code == 200 and data.get('features'):
            # GeoJSON structure: features[0].geometry.coordinates -> [lon, lat]
            coordinates = data['features'][0]['geometry']['coordinates']
            return coordinates # Returns [lon, lat]
            
        print(f"[Warning] Could not geocode '{place_name}'")
        return None
    except Exception as e:
        print(f"[Error] Geocoding error for '{place_name}': {e}")
        return None

def get_distance_by_coords(api_key, origin_coords, dest_coords):
    """
    Fetches the driving distance (in meters) between two [lon, lat] coordinate pairs.
    """
    if not api_key or api_key == "YOUR_API_KEY":
        return 1000 # Default mock
        
    matrix_url = "https://api.openrouteservice.org/v2/matrix/driving-car"
    headers = {
        'Authorization': api_key,
        'Content-Type': 'application/json; charset=utf-8'
    }
    payload = {
        "locations": [origin_coords, dest_coords],
        "metrics": ["distance"],
        "units": "m"
    }

    try:
        response = requests.post(matrix_url, json=payload, headers=headers)
        data = response.json()
        if response.status_code == 200:
            dist = data['distances'][0][1]
            return dist if dist is not None else float('inf')
        return float('inf')
    except:
        return float('inf')

def get_distance(api_key, origin_name, destination_name):
    """
    Fetches the driving distance (in meters) between two places.
    1. Geocodes name -> coordinates
    2. Calls Matrix API
    """
    
    # ---------------------------------------------------------
    # MOCK MODE
    # ---------------------------------------------------------
    if not api_key or api_key == "YOUR_API_KEY":
        return (len(origin_name) + len(destination_name)) * 500

    # ---------------------------------------------------------
    # REAL API MODE
    # ---------------------------------------------------------
    origin_coords = get_coordinates(api_key, origin_name)
    dest_coords = get_coordinates(api_key, destination_name)
    
    if not origin_coords or not dest_coords:
        return float('inf')

    return get_distance_by_coords(api_key, origin_coords, dest_coords)
