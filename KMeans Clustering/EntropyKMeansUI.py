from BaseClusteringUI import BaseClusteringUI
from EntropyKMeansClustering import EntropyKMeansClustering
import tkinter as tk
from tkinter import ttk

class EntropyKMeansUI(BaseClusteringUI):
    def __init__(self, root):
        # Create neighborhood size control first
        self.neighborhood_size = ttk.Spinbox(None, from_=2, to=20, width=5)
        self.neighborhood_size.set(5)  # Default value
        
        # Then call parent's init
        super().__init__(root, title="Entropy-based K-Means Clustering UI", mode="entropy")
        
        # Create the actual control in the UI
        self.create_neighborhood_control()
        
    def create_neighborhood_control(self):
        # Create a frame for neighborhood size control
        neighborhood_frame = ttk.Frame(self.main_frame)
        neighborhood_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Add label and spinbox for neighborhood size
        ttk.Label(neighborhood_frame, text="Neighborhood Size:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.neighborhood_size.grid(row=0, column=1, sticky=tk.W, pady=2)
        
        # Add update button for neighborhood size
        self.update_neighborhood_btn = ttk.Button(neighborhood_frame, text="Update Neighborhood", 
                                                command=self.update_plot)
        self.update_neighborhood_btn.grid(row=1, column=0, columnspan=2, pady=5)
        
    def update_plot(self):
        try:
            k = int(self.k_value.get())
            neighborhood_size = int(self.neighborhood_size.get())
            self.current_k = k
            
            # Clear the plot
            self.ax.clear()
            
            # Run Entropy K-means
            kmeans = EntropyKMeansClustering(k=k)
            kmeans.set_weights(self.capacitances)
            self.current_labels = kmeans.fit(self.points, neighborhood_size=neighborhood_size)
            
            # Plot data points with cluster colors
            scatter = self.ax.scatter(self.points[:, 0], self.points[:, 1], 
                                    c=self.current_labels, cmap='rainbow', alpha=0.5)
            
            # Plot centroids
            self.ax.scatter(kmeans.centroids[:, 0], kmeans.centroids[:, 1], 
                          c='black', marker='x', s=200, label='Centroids')
            
            # Update centroid display
            self.centroid_text.delete(1.0, tk.END)
            self.centroid_text.insert(tk.END, f"K = {k}\n")
            self.centroid_text.insert(tk.END, f"Neighborhood Size = {neighborhood_size}\n\n")
            for i, centroid in enumerate(kmeans.centroids):
                self.centroid_text.insert(tk.END, f"Centroid {i+1}:\n")
                self.centroid_text.insert(tk.END, f"X: {centroid[0]:.4f}\n")
                self.centroid_text.insert(tk.END, f"Y: {centroid[1]:.4f}\n\n")
            
            self.ax.set_title(f'Entropy-based K-Means Clustering (K={k}, N={neighborhood_size})')
            self.ax.set_xlabel('X')
            self.ax.set_ylabel('Y')
            self.ax.legend()
            
            # Update canvas
            self.canvas.draw()
            
        except ValueError as e:
            print(f"Error: {e}")

def main():
    root = tk.Tk()
    app = EntropyKMeansUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 