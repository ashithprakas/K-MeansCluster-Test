import numpy as np
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt

def calculate_entropy(data_points, neighborhood_size=5):
    """Calculate entropy for each point based on its neighborhood"""
    n_points = data_points.shape[0]
    entropies = np.zeros(n_points)
    
    # Calculate pairwise distances
    distances = cdist(data_points, data_points)
    
    for i in range(n_points):
        # Get k-nearest neighbors
        neighbor_indices = np.argsort(distances[i])[1:neighborhood_size+1]  # Exclude self
        neighbor_distances = distances[i][neighbor_indices]
        
        # Calculate probabilities based on distances using softmax
        exp_distances = np.exp(-neighbor_distances)
        probabilities = exp_distances / np.sum(exp_distances)
        
        # Calculate Shannon entropy
        entropy = -np.sum(probabilities * np.log(probabilities + 1e-10))
        entropies[i] = entropy
        
    return entropies

def plot_entropy_example():
    # Create example data points
    # Case 1: Points in a tight cluster
    tight_cluster = np.random.normal(0, 0.1, (20, 2))
    
    # Case 2: Points in a loose cluster
    loose_cluster = np.random.normal(0, 0.5, (20, 2))
    
    # Case 3: Points in a uniform distribution
    uniform_points = np.random.uniform(-1, 1, (20, 2))
    
    # Combine all points
    all_points = np.vstack([tight_cluster, loose_cluster, uniform_points])
    
    # Calculate entropies
    entropies = calculate_entropy(all_points)
    
    # Create plot
    plt.figure(figsize=(15, 5))
    
    # Plot 1: Original points
    plt.subplot(131)
    plt.scatter(all_points[:20, 0], all_points[:20, 1], c='blue', label='Tight Cluster')
    plt.scatter(all_points[20:40, 0], all_points[20:40, 1], c='red', label='Loose Cluster')
    plt.scatter(all_points[40:, 0], all_points[40:, 1], c='green', label='Uniform')
    plt.title('Original Points')
    plt.legend()
    
    # Plot 2: Entropy values
    plt.subplot(132)
    scatter = plt.scatter(all_points[:, 0], all_points[:, 1], 
                         c=entropies, cmap='viridis')
    plt.colorbar(scatter, label='Entropy')
    plt.title('Entropy Values')
    
    # Plot 3: Combined weights (if we had capacitance weights)
    plt.subplot(133)
    # Simulate capacitance weights (higher in tight cluster)
    weights = np.ones(len(all_points))
    weights[:20] = 2.0  # Higher weights for tight cluster
    combined_weights = weights * (1 + entropies)
    combined_weights = combined_weights / np.sum(combined_weights)
    
    scatter = plt.scatter(all_points[:, 0], all_points[:, 1], 
                         c=combined_weights, cmap='viridis')
    plt.colorbar(scatter, label='Combined Weight')
    plt.title('Combined Weights (Capacitance × (1 + Entropy))')
    
    plt.tight_layout()
    plt.savefig('entropy_example.png')
    plt.close()

if __name__ == "__main__":
    plot_entropy_example() 