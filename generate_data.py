import random
import osmnx as ox
from geopy.distance import great_circle
import csv
import os
class City:
    def __init__(self, name):
        graph_file = "nyc_graph.graphml"
        self.G = ox.load_graphml(graph_file)
        self.nodes = list(self.G.nodes())

    def generate_random_coordinates(self):
        node = random.choice(self.nodes)
        return self.G.nodes[node]['y'], self.G.nodes[node]['x']

    # Function to calculate a route between two points
    def calculate_route(self, start_coords, end_coords):
        origin = ox.distance.nearest_nodes(self.G, start_coords[0], start_coords[1])
        destination = ox.distance.nearest_nodes(self.G, end_coords[0], end_coords[1])
        route = ox.distance.shortest_path(self.G, origin, destination, weight='length')
        return route

# Set a location (New York City)
location = "New York City, New York, USA"

# Create synthetic data
num_rides = 1  # Adjust the number of rides as needed


graph_file = "nyc_graph.graphml"
if not os.path.exists(graph_file):
    G = ox.graph_from_place(location, network_type="drive")
    ox.save_graphml(G, filepath=graph_file)
NYC = City(location)

rides_data = []
for _ in range(num_rides):
    start_coords = NYC.generate_random_coordinates()
    end_coords = NYC.generate_random_coordinates()
    route = NYC.calculate_route(start_coords, end_coords)
    ride_data = {
        "start_latitude": start_coords[0],
        "start_longitude": start_coords[1],
        "end_latitude": end_coords[0],
        "end_longitude": end_coords[1],
        "route_coordinates": route
    }
    rides_data.append(ride_data)
    print(ride_data)

    # Create a Folium map for the route
    route_map = ox.plot_graph_folium(NYC.G, route=route)

    # Save the route map to an HTML file with a unique name
    route_map.save(f'route_{start_coords}.html')


route_map = ox.plot_route_folium(G, route)
route_map.save('test.html')
# You can save the data as needed (e.g., in a CSV file)

# Save the data to a CSV file
csv_file = 'rides_data.csv'

with open(csv_file, 'w', newline='') as csvfile:
    fieldnames = ["start_latitude", "start_longitude", "end_latitude", "end_longitude", "route_coordinates"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for ride in rides_data:
        writer.writerow(ride)

print(f"Data saved to {csv_file}")