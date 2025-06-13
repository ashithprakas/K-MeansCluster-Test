import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from FileReader import XYCoordinateExtractor
from KMeansClusteringHelper import KMenasClustering

class KMeansUI:
    def __init__(self, root):
        self.root = root
        self.root.title("K-Means Clustering Interactive UI")
        
        # Load data
        self.extractor = XYCoordinateExtractor("data.txt")
        self.points = np.array(self.extractor.extract_coordinates())
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create controls
        self.create_controls()
        
        # Create plot area
        self.create_plot_area()
        
        # Create centroid display area
        self.create_centroid_display()
        
        # Initial plot
        self.update_plot()

    def create_controls(self):
        # K value control
        ttk.Label(self.main_frame, text="K Value:").grid(row=0, column=0, sticky=tk.W)
        self.k_value = ttk.Spinbox(self.main_frame, from_=2, to=20, width=5)
        self.k_value.set(3)
        self.k_value.grid(row=0, column=1, sticky=tk.W)
        
        # Update button
        self.update_btn = ttk.Button(self.main_frame, text="Update Plot", command=self.update_plot)
        self.update_btn.grid(row=1, column=0, columnspan=2, pady=10)

    def create_plot_area(self):
        # Create figure for plotting
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_frame)
        self.canvas.get_tk_widget().grid(row=0, column=2, rowspan=4, padx=10)

    def create_centroid_display(self):
        # Create frame for centroid display
        self.centroid_frame = ttk.LabelFrame(self.main_frame, text="Centroid Coordinates", padding="5")
        self.centroid_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Create text widget for displaying coordinates
        self.centroid_text = tk.Text(self.centroid_frame, height=10, width=30)
        self.centroid_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.centroid_frame, orient="vertical", command=self.centroid_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.centroid_text.configure(yscrollcommand=scrollbar.set)

    def update_plot(self):
        try:
            k = int(self.k_value.get())
            
            # Clear the plot
            self.ax.clear()
            
            # Run K-means
            kmeans = KMenasClustering(k=k)
            labels = kmeans.fit(self.points)
            
            # Plot data points with cluster colors
            scatter = self.ax.scatter(self.points[:, 0], self.points[:, 1], c=labels, cmap='rainbow', alpha=0.5)
            
            # Plot centroids
            self.ax.scatter(kmeans.centroids[:, 0], kmeans.centroids[:, 1], 
                          c='black', marker='x', s=200, label='Centroids')
            
            # Update centroid display
            self.centroid_text.delete(1.0, tk.END)
            self.centroid_text.insert(tk.END, f"K = {k}\n\n")
            for i, centroid in enumerate(kmeans.centroids):
                self.centroid_text.insert(tk.END, f"Centroid {i+1}:\n")
                self.centroid_text.insert(tk.END, f"X: {centroid[0]:.4f}\n")
                self.centroid_text.insert(tk.END, f"Y: {centroid[1]:.4f}\n\n")
            
            self.ax.set_title(f'K-Means Clustering (K={k})')
            self.ax.set_xlabel('X')
            self.ax.set_ylabel('Y')
            self.ax.legend()
            
            # Update canvas
            self.canvas.draw()
            
        except ValueError as e:
            print(f"Error: {e}")

def main():
    root = tk.Tk()
    app = KMeansUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 