import streamlit as st
import os
import pandas as pd
from dotenv import load_dotenv
from graph_builder import GraphBuilder
from dijkstra import dijkstra

# Page Config
st.set_page_config(page_title=" Delhi Routing", page_icon="🚖", layout="wide")

# Load environment variables
load_dotenv()

# Design Styling
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #ff4b4b;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

def format_time(seconds):
    if seconds < 60:
        return "< 1 min"
    minutes = int(seconds // 60)
    hours = minutes // 60
    minutes = minutes % 60
    if hours > 0:
        return f"{hours} hr {minutes} min"
    return f"{minutes} min"

@st.cache_resource
def initialize_graph():
    api_key = os.getenv("ORS_API_KEY")
    builder = GraphBuilder(api_key)
    graph, city_coords = builder.build_demo_graph()
    return graph, city_coords, sorted(list(builder.nodes))

def main():
    st.title("🚖 Uber-Style Delhi Routing System")
    st.write("Find the shortest path between Delhi's most famous landmarks using Dijkstra's Algorithm.")

    # Sidebar for Configuration
    st.sidebar.header("Settings")
    speed = st.sidebar.slider("Average Speed (km/h)", 10, 100, 30)
    
    # Initialize Data
    with st.spinner("Building the city map..."):
        graph, city_coords, locations = initialize_graph()

    # Layout
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Route Selection")
        source = st.selectbox("Select Start Location", locations, index=0)
        destination = st.selectbox("Select Destination", locations, index=1)
        
        if st.button("Calculate Route"):
            if source == destination:
                st.warning("Start and Destination are the same!")
            else:
                dist_meters, path = dijkstra(graph, source, destination)
                
                if dist_meters == float('inf'):
                    st.error(f"No direct route found between {source} and {destination} in our demo graph.")
                else:
                    distance_km = dist_meters / 1000.0
                    speed_mps = speed * (1000.0 / 3600.0)
                    travel_time_seconds = dist_meters / speed_mps
                    
                    st.success("Route Found!")
                    
                    # Display Results
                    st.metric("Total Distance", f"{distance_km:.2f} km")
                    st.metric("Estimated Time", format_time(travel_time_seconds))
                    
                    st.info(f"**Optimal Path:** {' → '.join(path)}")

    with col2:
        st.subheader("Delhi Landmarks Map")
        # Prepare data for map
        map_df = pd.DataFrame([
            {"name": name, "lon": coords[0], "lat": coords[1]} 
            for name, coords in city_coords.items()
        ])
        
        st.map(map_df)
        with st.expander("Show Location Coordinates"):
            st.table(map_df)

    st.divider()
    st.markdown("### 🧠 How it works")
    st.write("""
    1. **Graph Construction**: We model Delhi's locations as nodes and roads as edges.
    2. **Real-time Data**: Distances are fetched using the **OpenRouteService API**.
    3. **Shortest Path**: We use **Dijkstra's Algorithm** to find the most efficient route.
    4. **ETA Calculation**: Time is calculated as `Distance / Speed`.
    """)

if __name__ == "__main__":
    main()
