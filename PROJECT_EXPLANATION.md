# 📌 Delhi Routing System - Project Explanation

## 🧠 System Overview
This project simulates how navigation apps like Google Maps or Uber calculate the best route for you. We focus on **Delhi's top 10 landmarks** to demonstrate the core logic.

The system now features a **Streamlit Web Interface**, providing a modern, interactive way to select routes and view results on a map.

## 🏗️ Architecture
The system is built with four main components, working together like a factory line:

1.  **Map Data (API Layer)**: `maps_api.py`
    *   This component acts as our "eyes". It uses the **OpenRouteService API**.
    *   First, it converts names (like "Central Station") into coordinates (Latitude/Longitude) using the **Geocoding API**.
    *   Then, it asks the **Matrix API**: "How far is it to drive between these two coordinates?"
    *   In our code, we also added a "Mock Mode" so you can play with it if the key isn't set up.

2.  **The Graph (Data Structure)**: `graph_builder.py`
    *   Computers don't see maps like we do; they see **Nodes** (dots) and **Edges** (lines).
    *   This file takes the list of places and the distances between them to build a mathematical structure called a **Graph**.
    *   *Analogy*: Think of it like connecting cities with strings, where the length of the string is the distance.

3.  **The Brain (Algorithm)**: `dijkstra.py`
    *   This is the smartest part of the system. It implements **Dijkstra's Algorithm**.
    *   It systematically explores paths from the start point, always ensuring it finds the absolute shortest way before moving further.
    *   *Why this algorithm?* It guarantees the mathematically shortest path and is the foundation of almost all routing software.

4.  **The Interface (Main App)**: `main.py`
    *   The conductor of the orchestra. It asks you where you want to go, builds the map, calls the "Brain" to solve the path, and then calculates how long it will take based on your speed.

---

## 🧮 How Dijkstra's Algorithm Works (Simplified)
Imagine you are in a maze and want to find the exit.
1.  **Start at the entrance.** Mark your distance as 0. Mark all other points as "Infinity" (unknown).
2.  **Look at neighbors.** If the neighbor is 5 meters away, update its distance to 5.
3.  **Pick the closest unvisited spot.** Go there.
4.  **Repeat.** From the new spot, look at *its* neighbors. If you find a shortcut to a place you already knew about (e.g., getting there in 8 meters instead of 10), update it!
5.  **Done.** When you reach the destination, valid math proves you found the shortest way.

## 🔁 Step-by-Step Execution Flow
1.  **User Input**: You choose "Home" -> "Office" and say you drive at "50 km/h".
2.  **Graph Construction**: The code simulates roads between landmarks (e.g., Home->Park, Park->Office).
3.  **Pathfinding**: `dijkstra.py` calculates that `Home -> Park -> Office` is 5km.
4.  **ETA Calculation**: `Time = Distance / Speed`. `5km / 50km/h = 0.1 hours` (6 mins).
5.  **Output**: You see the route and the time on screen.

## 🚀 Future Improvements
To make this more advanced, you could:
*   Add **Traffic Data**: Multiply the edge weights by a "traffic factor" (e.g., heavy traffic makes a short road "expensive").
*   **Turn-by-Turn**: Store instructions (e.g., "Turn Left") along with the distances.
*   **Real Map Visualization**: Use a library like `folium` to draw the line on a real map HTML file.
