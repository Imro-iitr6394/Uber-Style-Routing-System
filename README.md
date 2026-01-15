# Uber-Style Routing System 🚖

A Python-based navigation tool that calculates the shortest path between 10 famous Delhi landmarks using Dijkstra's Algorithm and OpenRouteService data.

## 📂 Project Structure
*   `app.py`: **New!** The Streamlit Web Interface.
*   `main.py`: The CLI version of the program.
*   `maps_api.py`: Connects to OpenRouteService API.
*   `graph_builder.py`: Organizes the Delhi map data.
*   `dijkstra.py`: The routing logic.
*   `PROJECT_EXPLANATION.md`: Detailed architecture guide.
*   `.env`: Stores your API Key.

## 🚀 How to Run
1.  **Install Requirements**:
    ```bash
    pip install -r uber_style_routing/requirements.txt
    ```

2.  **Run the Web App (Recommended)**:
    ```bash
    streamlit run uber_style_routing/app.py
    ```

3.  **Run the CLI (Optional)**:
    ```bash
    python uber_style_routing/main.py
    ```

## 🔑 OpenRouteService API
The project uses the key provided in the `.env` file.

*Enjoy your routing engine!*
