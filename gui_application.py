import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import webbrowser
import os
from city_tour_optimizer import CityTourOptimizer

class CityTourOptimizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("City Tour Optimizer")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        self.optimizer = None
        self.csv_path = None
        self.interactive_map_path = "tour_route_interactive.html"
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Style configuration
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 11))
        style.configure('TLabel', font=('Arial', 11))
        style.configure('Header.TLabel', font=('Arial', 14, 'bold'))
        
        # Title
        ttk.Label(main_frame, text="City Tour Optimizer", style='Header.TLabel').pack(pady=10)
        
        # Control Frame (left side)
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # File selection
        file_frame = ttk.Frame(control_frame)
        file_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(file_frame, text="City CSV File:").pack(anchor=tk.W)
        
        file_select_frame = ttk.Frame(file_frame)
        file_select_frame.pack(fill=tk.X, pady=5)
        
        self.file_path_var = tk.StringVar()
        ttk.Entry(file_select_frame, textvariable=self.file_path_var, width=25).pack(side=tk.LEFT, expand=True, fill=tk.X)
        ttk.Button(file_select_frame, text="Browse", command=self.browse_file).pack(side=tk.RIGHT, padx=5)
        
        # Create sample data button
        ttk.Button(file_frame, text="Create Sample Data", command=self.create_sample_data).pack(anchor=tk.W, pady=5)
        
        # City list
        ttk.Label(control_frame, text="Cities:").pack(anchor=tk.W, pady=(10, 2))
        
        city_frame = ttk.Frame(control_frame)
        city_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.city_listbox = tk.Listbox(city_frame, height=12, width=25, selectmode=tk.SINGLE)
        self.city_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        city_scrollbar = ttk.Scrollbar(city_frame, orient=tk.VERTICAL, command=self.city_listbox.yview)
        city_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.city_listbox.config(yscrollcommand=city_scrollbar.set)
        
        # Buttons
        process_frame = ttk.Frame(control_frame)
        process_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(process_frame, text="Load Cities", command=self.load_cities).pack(fill=tk.X, pady=2)
        ttk.Button(process_frame, text="Fetch Coordinates", command=self.fetch_coordinates).pack(fill=tk.X, pady=2)
        ttk.Button(process_frame, text="Optimize Route", command=self.optimize_route).pack(fill=tk.X, pady=2)
        
        visualization_frame = ttk.LabelFrame(control_frame, text="Visualization")
        visualization_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(visualization_frame, text="Static Map (Matplotlib)", command=self.show_static_map).pack(fill=tk.X, pady=2)
        ttk.Button(visualization_frame, text="Interactive Map (Folium)", command=self.create_interactive_map).pack(fill=tk.X, pady=2)
        ttk.Button(visualization_frame, text="Open Interactive Map", command=self.open_interactive_map).pack(fill=tk.X, pady=2)
        
        # Output and visualization frame (right side)
        output_frame = ttk.LabelFrame(main_frame, text="Output & Visualization", padding="10")
        output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Log output
        ttk.Label(output_frame, text="Log:").pack(anchor=tk.W)
        
        log_frame = ttk.Frame(output_frame)
        log_frame.pack(fill=tk.X, pady=5)
        
        self.log_text = tk.Text(log_frame, height=10, width=40, wrap=tk.WORD)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        log_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=log_scrollbar.set)
        
        # Route details
        ttk.Label(output_frame, text="Optimized Route:").pack(anchor=tk.W, pady=(10, 0))
        
        route_frame = ttk.Frame(output_frame)
        route_frame.pack(fill=tk.X, pady=5)
        
        self.route_text = tk.Text(route_frame, height=6, width=40, wrap=tk.WORD)
        self.route_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        route_scrollbar = ttk.Scrollbar(route_frame, orient=tk.VERTICAL, command=self.route_text.yview)
        route_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.route_text.config(yscrollcommand=route_scrollbar.set)
        
        # Map visualization area
        self.map_frame = ttk.Frame(output_frame)
        self.map_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def log(self, message):
        """Append a message to the log text area"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def update_status(self, message):
        """Update the status bar message"""
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def browse_file(self):
        """Open a file dialog to select a CSV file"""
        filepath = filedialog.askopenfilename(
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if filepath:
            self.file_path_var.set(filepath)
            self.csv_path = filepath
    
    def create_sample_data(self):
        """Create a sample CSV file with Indian cities"""
        try:
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
            
            filepath = "cities.csv"
            df.to_csv(filepath, index=False, header=False)
            
            self.log(f"Created sample CSV with {len(indian_cities)} Indian cities")
            self.file_path_var.set(filepath)
            self.csv_path = filepath
            
            messagebox.showinfo("Success", f"Sample data created at {filepath}")
        except Exception as e:
            self.log(f"Error creating sample data: {e}")
            messagebox.showerror("Error", f"Failed to create sample data: {e}")
    
    def load_cities(self):
        """Load cities from the selected CSV file"""
        if not self.csv_path:
            messagebox.showwarning("Warning", "Please select a CSV file first.")
            return
        
        try:
            self.optimizer = CityTourOptimizer(self.csv_path)
            
            # Update city listbox
            self.city_listbox.delete(0, tk.END)
            for city in self.optimizer.cities:
                self.city_listbox.insert(tk.END, city)
            
            self.log(f"Loaded {len(self.optimizer.cities)} cities from {self.csv_path}")
            self.update_status(f"{len(self.optimizer.cities)} cities loaded")
        except Exception as e:
            self.log(f"Error loading cities: {e}")
            messagebox.showerror("Error", f"Failed to load cities: {e}")
    
    def run_in_thread(self, func, success_msg):
        """Run a function in a separate thread to prevent UI freezing"""
        def thread_func():
            try:
                func()
                self.root.after(0, lambda: self.update_status(success_msg))
            except Exception as e:
                error_msg = str(e)
                self.root.after(0, lambda: self.log(f"Error: {error_msg}"))
                self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
            finally:
                self.root.after(0, lambda: self.update_status("Ready"))
        
        threading.Thread(target=thread_func, daemon=True).start()
    
    def fetch_coordinates(self):
        """Fetch geographic coordinates for all cities"""
        if not self.optimizer:
            messagebox.showwarning("Warning", "Please load cities first.")
            return
        
        self.update_status("Fetching coordinates...")
        self.log("Fetching coordinates for all cities...")
        
        # Run in a separate thread to prevent UI freezing
        self.run_in_thread(
            self.optimizer.fetch_coordinates,
            "Coordinates fetched successfully"
        )
    
    def optimize_route(self):
        """Calculate the optimized route using TSP"""
        if not self.optimizer:
            messagebox.showwarning("Warning", "Please load cities first.")
            return
        
        if not self.optimizer.coordinates:
            messagebox.showwarning("Warning", "Please fetch coordinates first.")
            return
        
        self.update_status("Optimizing route...")
        self.log("Calculating distance matrix and optimizing route...")
        
        def optimize():
            self.optimizer.calculate_distance_matrix()
            self.optimizer.nearest_neighbor_tsp()
            
            # Update route text
            self.root.after(0, self.update_route_text)
        
        # Run in a separate thread
        self.run_in_thread(optimize, "Route optimization complete")
    
    def update_route_text(self):
        """Update the route details in the text widget"""
        if not self.optimizer or not self.optimizer.optimized_route:
            return
        
        self.route_text.delete(1.0, tk.END)
        
        route_text = f"Optimized Tour Route\n"
        route_text += f"Starting from: {self.optimizer.cities[self.optimizer.optimized_route[0]]}\n\n"
        
        for i in range(1, len(self.optimizer.optimized_route)):
            from_idx = self.optimizer.optimized_route[i-1]
            to_idx = self.optimizer.optimized_route[i]
            from_city = self.optimizer.cities[from_idx]
            to_city = self.optimizer.cities[to_idx]
            distance = self.optimizer.distance_matrix[from_idx][to_idx]
            
            route_text += f"{i}. {from_city} → {to_city} ({distance:.2f} km)\n"
        
        route_text += f"\nTotal tour distance: {self.optimizer.total_distance:.2f} km\n"
        route_text += f"Number of cities visited: {len(self.optimizer.cities)}"
        
        self.route_text.insert(tk.END, route_text)
    
    def show_static_map(self):
        """Display the static map using Matplotlib in the GUI"""
        if not self.optimizer or not self.optimizer.optimized_route:
            messagebox.showwarning("Warning", "Please optimize the route first.")
            return
        
        # Clear any existing plot
        for widget in self.map_frame.winfo_children():
            widget.destroy()
        
        # Create figure
        fig = plt.Figure(figsize=(6, 5), dpi=100)
        ax = fig.add_subplot(111)
        
        # Plot cities
        lats = [self.optimizer.coordinates[city][0] for city in self.optimizer.cities]
        lons = [self.optimizer.coordinates[city][1] for city in self.optimizer.cities]
        ax.scatter(lons, lats, c='blue', s=50, label='Cities')
        
        # Plot route
        route_lats = []
        route_lons = []
        for idx in self.optimizer.optimized_route:
            city = self.optimizer.cities[idx]
            lat, lon = self.optimizer.coordinates[city]
            route_lats.append(lat)
            route_lons.append(lon)
        
        ax.plot(route_lons, route_lats, 'r-', linewidth=2, label='Optimized Route')
        
        # Mark start/end
        start_idx = self.optimizer.optimized_route[0]
        start_city = self.optimizer.cities[start_idx]
        start_lat, start_lon = self.optimizer.coordinates[start_city]
        ax.scatter(start_lon, start_lat, c='green', s=150, marker='*', label='Start/End')
        
        # Add city labels
        for city, (lat, lon) in self.optimizer.coordinates.items():
            ax.annotate(city, (lon, lat), fontsize=8, ha='right', va='bottom')
        
        ax.set_title('Optimized City Tour Route')
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        ax.grid(True)
        ax.legend()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.map_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.log("Static map displayed")
    
    def create_interactive_map(self):
        """Create an interactive map using Folium"""
        if not self.optimizer or not self.optimizer.optimized_route:
            messagebox.showwarning("Warning", "Please optimize the route first.")
            return
        
        self.update_status("Creating interactive map...")
        self.log("Generating interactive map...")
        
        def generate_map():
            self.optimizer.visualize_folium(self.interactive_map_path)
        
        # Run in a separate thread
        self.run_in_thread(
            generate_map,
            f"Interactive map created: {self.interactive_map_path}"
        )
    
    def open_interactive_map(self):
        """Open the interactive map in a web browser"""
        if not os.path.exists(self.interactive_map_path):
            messagebox.showwarning("Warning", "Please create an interactive map first.")
            return
        
        try:
            # Convert to absolute path for more reliable browser opening
            absolute_path = os.path.abspath(self.interactive_map_path)
            
            # Open in default web browser
            webbrowser.open(f"file://{absolute_path}")
            self.log(f"Opening map in browser: {self.interactive_map_path}")
        except Exception as e:
            self.log(f"Error opening map: {e}")
            messagebox.showerror("Error", f"Failed to open map: {e}")

def main():
    root = tk.Tk()
    app = CityTourOptimizerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()