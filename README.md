# City Tour Optimizer:- Project Documentation

## Project Overview
The City Tour Optimizer is a Python application that finds the shortest possible route for visiting multiple Indian cities using the Traveling Salesman Problem (TSP) algorithm. The tool uses real-world geographic coordinates to calculate distances between cities, optimizes the route, and visualizes the results.

## Features
- Load city names from a CSV file
- Automatically fetch geographic coordinates using the `geopy` library
- Calculate distances between cities using the Haversine formula
- Optimize the tour route using the Nearest Neighbor algorithm
- Visualize the optimized route using both static (Matplotlib) and interactive (Folium) maps
- User-friendly GUI interface

## Project Structure
```
city_tour_optimizer/
├── city_tour_optimizer.py    # Core implementation class
├── demo_script.py            # Demo script for command-line demonstration
├── gui_application.py        # GUI application
├── cities.csv                # Sample input file (generated)
├── tour_route_static.png     # Static map visualization (generated)
└── tour_route_interactive.html # Interactive map visualization (generated)
```

## Installation

### Requirements
- Python 3.7+
- Required libraries: geopy, folium, matplotlib, pandas, tkinter

### Setup
1. Install the required Python packages:
   ```
   pip install geopy folium matplotlib pandas
   ```
   Note: tkinter is included with most Python installations.

2. Clone or download the project files to your local machine.

3. Run any of the following scripts to start the application:
   - For GUI: `python gui_application.py`
   - For demo: `python demo_script.py`

## How to Use

### Command-line Demo
Run `demo_script.py` to see a complete demonstration of the City Tour Optimizer. The script will:
1. Create a sample CSV with Indian cities (if it doesn't exist)
2. Load cities from the CSV
3. Fetch geographic coordinates for each city
4. Calculate the distance matrix
5. Optimize the tour route using TSP
6. Generate static and interactive visualizations

### GUI Application
The GUI application provides a user-friendly interface for interacting with the City Tour Optimizer:

1. Start the application: `python gui_application.py`
2. Load cities:
   - Create a sample dataset using the "Create Sample Data" button, or
   - Load a custom CSV file using the "Browse" button
3. Click "Load Cities" to load the cities from the selected CSV
4. Click "Fetch Coordinates" to retrieve geographic coordinates
5. Click "Optimize Route" to calculate the optimized tour
6. Visualize the results:
   - "Static Map" - Display a static map in the application
   - "Interactive Map" - Generate an interactive HTML map
   - "Open Interactive Map" - Open the interactive map in a web browser

### Input Format
The input CSV file should contain one city name per line. For example:
```
Mumbai
Delhi
Bangalore
Hyderabad
Chennai
```

## Implementation Details

### Core Components

#### 1. `CityTourOptimizer` Class
The main class that implements the core functionality:
- Loading cities from CSV
- Fetching coordinates using geopy
- Calculating distances using the Haversine formula
- Implementing the Nearest Neighbor algorithm for TSP
- Generating visualizations using Matplotlib and Folium

#### 2. Demo Script
A command-line demonstration script that showcases the entire workflow.

#### 3. GUI Application
A tkinter-based GUI that provides a user-friendly interface for the City Tour Optimizer.

### Algorithms

#### Haversine Formula
The Haversine formula calculates the great-circle distance between two points on a sphere, given their longitude and latitude:

```
a = sin²(Δlat/2) + cos(lat1) * cos(lat2) * sin²(Δlon/2)
c = 2 * atan2(√a, √(1-a))
d = R * c
```
Where:
- Δlat is the difference in latitude
- Δlon is the difference in longitude
- R is the Earth's radius (6371 km)

#### Nearest Neighbor Algorithm
A greedy algorithm for TSP that iteratively builds a path by selecting the nearest unvisited city:
1. Start at a random city
2. Find the nearest unvisited city and move there
3. Repeat until all cities are visited
4. Return to the starting city

## Future Enhancements
- Implement more advanced TSP algorithms (genetic algorithms, simulated annealing)
- Add optimization parameters (time constraints, priority cities)
- Support for multiple transportation modes
- Export routes to different formats (GPX, KML)
- Integration with mapping services (Google Maps, OpenStreetMap)

## Credits and References
- Haversine formula: [Movable Type Scripts](https://www.movable-type.co.uk/scripts/latlong.html)
- TSP algorithms: [Traveling Salesman Problem - Wikipedia](https://en.wikipedia.org/wiki/Travelling_salesman_problem)
- Python libraries:
  - [geopy](https://geopy.readthedocs.io/): Geocoding library
  - [folium](https://python-visualization.github.io/folium/): Interactive maps
  - [matplotlib](https://matplotlib.org/): Static visualization
  - [pandas](https://pandas.pydata.org/): Data manipulation
