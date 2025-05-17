import os
import pandas as pd
from city_tour_optimizer import CityTourOptimizer

def create_sample_csv():
    """Create a sample CSV file with Indian cities if it doesn't exist"""
    if not os.path.exists("cities.csv"):
        # List of major Indian cities
        indian_cities = [
            "Mumbai",
            "Delhi",
            "Bangalore",
            "Hyderabad",
            "Chennai",
            "Kolkata",
            "Jaipur",
            "Ahmedabad",
            "Pune",
            "Lucknow",
            "Kochi",
            "Chandigarh",
            "Goa"
        ]
        
        # Create a DataFrame and save as CSV
        df = pd.DataFrame(indian_cities, columns=["City"])
        df.to_csv("cities.csv", index=False, header=False)
        print(f"Created sample CSV with {len(indian_cities)} Indian cities")
        return True
    else:
        print("cities.csv already exists. Using existing file.")
        return False

def run_demo():
    """Run a complete demonstration of the City Tour Optimizer"""
    print("=" * 50)
    print("CITY TOUR OPTIMIZER - TSP DEMO")
    print("=" * 50)
    
    # Create sample data if needed
    create_sample_csv()
    
    # Initialize the optimizer
    optimizer = CityTourOptimizer("cities.csv")
    
    print("\n1. FETCHING CITY COORDINATES...")
    optimizer.fetch_coordinates()
    
    print("\n2. CALCULATING DISTANCE MATRIX...")
    optimizer.calculate_distance_matrix()
    
    print("\n3. OPTIMIZING ROUTE WITH TSP...")
    optimizer.nearest_neighbor_tsp()
    optimizer.print_optimized_route()
    
    print("\n4. GENERATING VISUALIZATIONS...")
    print("- Creating static map (Matplotlib)...")
    optimizer.visualize_matplotlib("tour_route_static.png")
    
    print("- Creating interactive map (Folium)...")
    interactive_map = optimizer.visualize_folium("tour_route_interactive.html")
    
    print("\n" + "=" * 50)
    print("DEMO COMPLETE!")
    print("=" * 50)
    print("\nOutput files generated:")
    print("- tour_route_static.png (Static map)")
    print("- tour_route_interactive.html (Interactive map)")
    print("\nOpen the HTML file in a web browser to view the interactive map.")

if __name__ == "__main__":
    run_demo()