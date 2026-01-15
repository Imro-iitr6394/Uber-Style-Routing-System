import heapq

def dijkstra(graph, start_node, end_node):
    """
    Finds the shortest path between start_node and end_node in the graph.
    
    Args:
        graph: Dictionary representing the graph {node: {neighbor: weight}}
        start_node: The starting location name
        end_node: The destination location name
        
    Returns:
        tuple: (shortest_distance, path_list)
        If no path exists, returns (infinity, [])
    """
    
    # Priority Queue to store (current_distance, current_node)
    # Allows us to always expand the cheapest node first
    queue = [(0, start_node)]
    
    # Dictionary to track the shortest distance found so far to each node
    distances = {node: float('inf') for node in graph}
    distances[start_node] = 0
    
    # Dictionary to reconstruct the path (stores where we came from)
    previous_nodes = {node: None for node in graph}
    
    visited = set()

    while queue:
        current_distance, current_node = heapq.heappop(queue)
        
        # Optimization: If we reached the destination, we can stop early
        if current_node == end_node:
            break
            
        if current_node in visited:
            continue
        visited.add(current_node)
        
        # Explore neighbors
        if current_node in graph:
            for neighbor, weight in graph[current_node].items():
                distance = current_distance + weight
                
                # If we found a shorter path to the neighbor, update it
                if distance < distances.get(neighbor, float('inf')):
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(queue, (distance, neighbor))
    
    # Reconstruct path by backtracking
    path = []
    current = end_node
    
    # Check if a path was actually found
    if distances.get(end_node) == float('inf'):
        return float('inf'), []
        
    while current is not None:
        path.insert(0, current)
        current = previous_nodes[current]
        
    return distances[end_node], path
