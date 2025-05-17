import csv
import math
import folium
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time

class CityTourOptimizer:
    def __init__(self, csv_file=None):
        self.cities = []
        self.coordinates = {}
        self.distance_matrix = []
        self.optimized_route = []
        self.total_distance = 0
        
        if csv_file:
            self.load_cities_from_csv(csv_file)
    
    def load_cities_from_csv(self, csv_file):
        """Load city names from a CSV file"""
        try:
            with open(csv_file, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row:  # Check if row is not empty
                        city = row[0].strip()
                        if city and city not in self.cities:
                            self.cities.append(city)
            print(f"Loaded {len(self.cities)} cities from {csv_file}")
        except FileNotFoundError:
            print(f"Error: File {csv_file} not found")
        except Exception as e:
            print(f"Error reading CSV file: {e}")
    
    def fetch_coordinates(self):
        """Fetch geographical coordinates for each city"""
        geolocator = Nominatim(user_agent="city_tour_optimizer")
        
        for city in self.cities:
            tries = 0
            max_tries = 3
            
            while tries < max_tries:
                try:
                    # Add ", India" to ensure we get Indian cities
                    location = geolocator.geocode(f"{city}, India")
                    if location:
                        self.coordinates[city] = (location.latitude, location.longitude)
                        print(f"Found coordinates for {city}: {self.coordinates[city]}")
                        break
                    else:
                        print(f"Warning: Could not find coordinates for {city}")
                        break
                except (GeocoderTimedOut, GeocoderServiceError):
                    tries += 1
                    if tries == max_tries:
                        print(f"Error: Failed to fetch coordinates for {city} after {max_tries} attempts")
                    else:
                        print(f"Timeout fetching coordinates for {city}. Retrying ({tries}/{max_tries})...")
                        time.sleep(1)  # Wait before retrying
                except Exception as e:
                    print(f"Error fetching coordinates for {city}: {e}")
                    break
            
            # If we couldn't get coordinates after all tries, remove the city
            if city not in self.coordinates:
                print(f"Removing {city} from the list due to missing coordinates")
                self.cities.remove(city)
        
        print(f"Successfully fetched coordinates for {len(self.coordinates)} cities")
    
    def haversine_distance(self, lat1, lon1, lat2, lon2):
        """Calculate the great circle distance between two points on earth (in km)"""
        # Convert decimal degrees to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        r = 6371  # Radius of earth in kilometers
        return c * r
    
    def calculate_distance_matrix(self):
        """Calculate the distance matrix between all cities"""
        n = len(self.cities)
        self.distance_matrix = [[0 for _ in range(n)] for _ in range(n)]
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    city_i = self.cities[i]
                    city_j = self.cities[j]
                    lat1, lon1 = self.coordinates[city_i]
                    lat2, lon2 = self.coordinates[city_j]
                    
                    distance = self.haversine_distance(lat1, lon1, lat2, lon2)
                    self.distance_matrix[i][j] = distance
        
        print("Distance matrix calculated successfully")
    
    def nearest_neighbor_tsp(self, start_city_index=0):
        """Implement the Nearest Neighbor algorithm for TSP"""
        n = len(self.cities)
        if n == 0:
            print("Error: No cities available for optimization")
            return
            
        # Initialize variables
        unvisited = set(range(n))
        current = start_city_index
        self.optimized_route = [current]
        self.total_distance = 0
        unvisited.remove(current)
        
        # Main loop to find the nearest unvisited city
        while unvisited:
            nearest = min(unvisited, key=lambda city: self.distance_matrix[current][city])
            self.total_distance += self.distance_matrix[current][nearest]
            current = nearest
            self.optimized_route.append(current)
            unvisited.remove(nearest)
        
        # Return to the starting city
        self.total_distance += self.distance_matrix[current][start_city_index]
        self.optimized_route.append(start_city_index)
        
        print("Optimized route calculated using Nearest Neighbor algorithm")
        
    def print_optimized_route(self):
        """Print the optimized route with step-by-step details"""
        if not self.optimized_route:
            print("No optimized route available. Run the TSP algorithm first.")
            return
            
        print("\n--- Optimized Tour Route ---")
        print(f"Starting from: {self.cities[self.optimized_route[0]]}")
        
        for i in range(1, len(self.optimized_route)):
            from_idx = self.optimized_route[i-1]
            to_idx = self.optimized_route[i]
            from_city = self.cities[from_idx]
            to_city = self.cities[to_idx]
            distance = self.distance_matrix[from_idx][to_idx]
            
            print(f"{i}. {from_city} → {to_city} ({distance:.2f} km)")
        
        print(f"\nTotal tour distance: {self.total_distance:.2f} km")
        print(f"Number of cities visited: {len(self.cities)}")
    
    def visualize_matplotlib(self, save_path=None):
        """Create a static visualization of the optimized route using Matplotlib"""
        if not self.optimized_route:
            print("No optimized route available. Run the TSP algorithm first.")
            return
        
        plt.figure(figsize=(12, 10))
        
        # Plot all cities
        lats = [self.coordinates[city][0] for city in self.cities]
        lons = [self.coordinates[city][1] for city in self.cities]
        plt.scatter(lons, lats, c='blue', s=50, label='Cities')
        
        # Plot the optimized route
        route_lats = []
        route_lons = []
        for idx in self.optimized_route:
            city = self.cities[idx]
            lat, lon = self.coordinates[city]
            route_lats.append(lat)
            route_lons.append(lon)
        
        plt.plot(route_lons, route_lats, 'r-', linewidth=2, label='Optimized Route')
        
        # Mark the starting city
        start_idx = self.optimized_route[0]
        start_city = self.cities[start_idx]
        start_lat, start_lon = self.coordinates[start_city]
        plt.scatter(start_lon, start_lat, c='green', s=200, marker='*', label='Start/End City')
        
        # Add city labels
        for city, (lat, lon) in self.coordinates.items():
            plt.annotate(city, (lon, lat), fontsize=8, ha='right', va='bottom')
        
        plt.title('Optimized City Tour Route')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.grid(True)
        plt.legend()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Map saved to {save_path}")
        
        plt.show()
    
    def visualize_folium(self, save_path=None):
        """Create an interactive visualization of the optimized route using Folium"""
        if not self.optimized_route:
            print("No optimized route available. Run the TSP algorithm first.")
            return
        
        # Calculate center coordinates for the map
        center_lat = sum(coord[0] for coord in self.coordinates.values()) / len(self.coordinates)
        center_lon = sum(coord[1] for coord in self.coordinates.values()) / len(self.coordinates)
        
        # Create a map
        m = folium.Map(location=[center_lat, center_lon], zoom_start=6)
        
        # Add markers for each city
        for city, (lat, lon) in self.coordinates.items():
            tooltip = f"{city}"
            # Make the start/end city marker more prominent
            if city == self.cities[self.optimized_route[0]]:
                folium.Marker(
                    [lat, lon],
                    popup=f"{city} (Start/End)",
                    tooltip=tooltip,
                    icon=folium.Icon(color='green', icon='star')
                ).add_to(m)
            else:
                folium.Marker(
                    [lat, lon],
                    popup=city,
                    tooltip=tooltip,
                    icon=folium.Icon(color='blue')
                ).add_to(m)
        
        # Draw the optimized route
        route_points = []
        for idx in self.optimized_route:
            city = self.cities[idx]
            lat, lon = self.coordinates[city]
            route_points.append([lat, lon])
        
        folium.PolyLine(
            route_points,
            color='red',
            weight=2.5,
            opacity=1,
            tooltip="Optimized Route"
        ).add_to(m)
        
        # Add distance information
        route_info = f"Total Distance: {self.total_distance:.2f} km<br>Cities: {len(self.cities)}"
        title_html = f'<h3 align="center" style="font-size:16px"><b>Optimized City Tour</b><br>{route_info}</h3>'
        m.get_root().html.add_child(folium.Element(title_html))
        
        if save_path:
            m.save(save_path)
            print(f"Interactive map saved to {save_path}")
        
        return m

def main():
    # Example usage
    optimizer = CityTourOptimizer("cities.csv")
    optimizer.fetch_coordinates()
    optimizer.calculate_distance_matrix()
    optimizer.nearest_neighbor_tsp()
    optimizer.print_optimized_route()
    
    # Generate visualizations
    optimizer.visualize_matplotlib("tour_route_static.png")
    interactive_map = optimizer.visualize_folium("tour_route_interactive.html")
    
    print("\nVisualization complete! Check the generated files.")

if __name__ == "__main__":
    main()