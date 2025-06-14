from BaseClusteringUI import BaseClusteringUI
from WeightedKMeansClustering import WeightedKMeansClustering
import tkinter as tk
from tkinter import ttk

class WeightedKMeansUI(BaseClusteringUI):
    def __init__(self, root):
        super().__init__(root, title="Weighted K-Means Clustering UI", mode="weighted")
        
    def update_plot(self):
        try:
            k = int(self.k_value.get())
            self.current_k = k
            
            # Clear the plot
            self.ax.clear()
            
            # Run Weighted K-means
            kmeans = WeightedKMeansClustering(k=k)
            # Set the weights using capacitance values

            kmeans.set_weights(self.capacitances)

            self.current_labels = kmeans.fit(self.points)
            
            # Plot data points with cluster colors
            scatter = self.ax.scatter(self.points[:, 0], self.points[:, 1], 
                                    c=self.current_labels, cmap='rainbow', alpha=0.5)
            
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
            
            self.ax.set_title(f'Weighted K-Means Clustering (K={k})')
            self.ax.set_xlabel('X')
            self.ax.set_ylabel('Y')
            self.ax.legend()
            
            # Update canvas
            self.canvas.draw()
            
        except ValueError as e:
            print(f"Error: {e}")

def main():
    root = tk.Tk()
    app = WeightedKMeansUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 