import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from FileReader import XYCoordinateExtractor
import os

class BaseClusteringUI:
    def __init__(self, root, title="Clustering UI", mode="regular"):
        self.root = root
        self.root.title(title)
        self.mode = mode
        
        # Create output directories if they don't exist
        self.output_dir = os.path.join("output", f"{mode}_kmeans")
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Load data
        self.extractor = XYCoordinateExtractor(
            os.path.join("input", "data.txt"),
            os.path.join("input", "capacitenceData.txt")
        )
        raw_points = self.extractor.extract_coordinates()
        # Convert list of dictionaries to numpy array of coordinates
        self.points = np.array([[point['x'], point['y']] for point in raw_points])
        self.labels = [point['label'] for point in raw_points]
        self.capacitances = [point['capacitance'] for point in raw_points]
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create controls
        self.create_controls()
        
        # Create plot area
        self.create_plot_area()
        
        # Create centroid display area
        self.create_centroid_display()
        
        # Store current clustering results
        self.current_labels = None
        self.current_k = None
        
        # Initial plot
        self.update_plot()

    def create_controls(self):
        # Create a frame for controls
        controls_frame = ttk.Frame(self.main_frame)
        controls_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        # K value control
        ttk.Label(controls_frame, text="K Value:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.k_value = ttk.Spinbox(controls_frame, from_=2, to=20, width=5)
        self.k_value.set(3)
        self.k_value.grid(row=0, column=1, sticky=tk.W, pady=2)
        
        # Update button
        self.update_btn = ttk.Button(controls_frame, text="Update Plot", command=self.update_plot)
        self.update_btn.grid(row=1, column=0, columnspan=2, pady=5)
        
        # Save clusters button
        self.save_btn = ttk.Button(controls_frame, text="Save Clusters", command=self.save_clusters)
        self.save_btn.grid(row=2, column=0, columnspan=2, pady=5)

    def create_plot_area(self):
        # Create figure for plotting
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_frame)
        self.canvas.get_tk_widget().grid(row=0, column=1, rowspan=2, padx=10, pady=5)

    def create_centroid_display(self):
        # Create frame for centroid display
        self.centroid_frame = ttk.LabelFrame(self.main_frame, text="Centroid Coordinates", padding="5")
        self.centroid_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Create text widget for displaying coordinates
        self.centroid_text = tk.Text(self.centroid_frame, height=10, width=30)
        self.centroid_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.centroid_frame, orient="vertical", command=self.centroid_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.centroid_text.configure(yscrollcommand=scrollbar.set)

    def update_plot(self):
        raise NotImplementedError("Subclasses must implement update_plot")

    def save_clusters(self):
        if self.current_labels is None:
            return
            
        k = self.current_k
        filename = os.path.join(self.output_dir, f"ClusterOutputk={k}.txt")
        
        try:
            with open(filename, 'w') as f:
                f.write(f"Cluster Assignments for {self.mode.title()} K-Means (K={k})\n")
                f.write("=" * 50 + "\n\n")
                
                # Group labels by cluster
                clusters = {}
                for label, cluster_id, point in zip(self.labels, self.current_labels, self.points):
                    if cluster_id not in clusters:
                        clusters[cluster_id] = []
                    clusters[cluster_id].append((label, point))
                
                # Get the current centroids from the plot
                centroids = self.ax.collections[-1].get_offsets()
                
                # Write each cluster's contents
                for cluster_id in sorted(clusters.keys()):
                    f.write(f"Cluster {cluster_id + 1}:\n")
                    f.write("-" * 20 + "\n")
                    f.write(f"Centroid Coordinates: X = {centroids[cluster_id][0]:.4f}, Y = {centroids[cluster_id][1]:.4f}\n")
                    f.write("-" * 20 + "\n")
                    f.write("Points in this cluster:\n")
                    for label, point in sorted(clusters[cluster_id]):
                        f.write(f"{label}: X = {point[0]:.4f}, Y = {point[1]:.4f}\n")
                    f.write("\n")
                    
            print(f"Successfully saved cluster assignments to {filename}")
        except Exception as e:
            print(f"Error saving clusters: {e}") 