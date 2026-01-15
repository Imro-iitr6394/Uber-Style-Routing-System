from maps_api import get_distance

class GraphBuilder:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.nodes = set()
        # Graph structure: { 'NodeA': {'NodeB': distance, 'NodeC': distance} }
        self.graph = {}

    def add_location(self, location_name):
        """Adds a location (node) to the graph."""
        self.nodes.add(location_name)
        if location_name not in self.graph:
            self.graph[location_name] = {}

    def add_route(self, origin, destination, one_way=False):
        """
        Adds a route (edge) between two locations.
        Fetches the real distance using the Maps API helper.
        """
        if origin not in self.nodes:
            self.add_location(origin)
        if destination not in self.nodes:
            self.add_location(destination)

        # distinct call to get weight
        dist = get_distance(self.api_key, origin, destination)
        
        self.graph[origin][destination] = dist
        print(f"Added route: {origin} -> {destination} = {dist} meters")

        if not one_way:
            # If bi-directional, typically travel distance might vary slightly,
            # but for simplicity we can fetch again or assume symmetric for this demo.
            # Let's fetch the reverse to be accurate to reality.
            dist_back = get_distance(self.api_key, destination, origin)
            self.graph[destination][origin] = dist_back

    def build_demo_graph(self):
        """
        Builds a predefined graph of Delhi locations using precise coordinates.
        This provides a realistic "Uber-style" experience in India's capital.
        """
        from maps_api import get_distance_by_coords

        print("--- Building Map Data (Delhi Cluster) ---")
        
        # [Longitude, Latitude] for Delhi's top landmarks
        city_coords = {
            "India Gate": [77.2295, 28.6129],
            "Red Fort": [77.2410, 28.6562],
            "Qutub Minar": [77.1855, 28.5244],
            "Lotus Temple": [77.2588, 28.5535],
            "Akshardham Temple": [77.2773, 28.6127],
            "Humayun's Tomb": [77.2507, 28.5933],
            "Jama Masjid": [77.2339, 28.6507],
            "Connaught Place": [77.2167, 28.6333],
            "Rashtrapati Bhavan": [77.1994, 28.6143],
            "Chandni Chowk": [77.2285, 28.6505]
        }
        
        # Add locations
        for loc in city_coords:
            self.add_location(loc)
        
        # Define Connections (Realistic road segments)
        routes = [
            ("India Gate", "Rashtrapati Bhavan"),
            ("India Gate", "Connaught Place"),
            ("India Gate", "Humayun's Tomb"),
            ("Red Fort", "Jama Masjid"),
            ("Red Fort", "Chandni Chowk"),
            ("Jama Masjid", "Chandni Chowk"),
            ("Connaught Place", "Red Fort"),
            ("Humayun's Tomb", "Lotus Temple"),
            ("Lotus Temple", "Akshardham Temple"),
            ("Lotus Temple", "Qutub Minar"),
            ("Rashtrapati Bhavan", "Connaught Place"),
            ("Akshardham Temple", "Red Fort")
        ]

        for u, v in routes:
            print(f"   > API: Fetching distance for {u} -> {v}...")
            dist = get_distance_by_coords(self.api_key, city_coords[u], city_coords[v])
            
            if dist != float('inf'):
                self.graph[u][v] = dist
                # Symmetric for this demo
                self.graph[v][u] = dist
            else:
                print(f"[Warning] No road found for {u} -> {v}")
        
        return self.graph, city_coords
