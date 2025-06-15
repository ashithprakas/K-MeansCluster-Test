import numpy as np
from scipy.spatial.distance import cdist

class EntropyKMeansClustering:
    def __init__(self, k=3, max_iterations=100, random_state=42):
        self.k = k
        self.max_iterations = max_iterations
        self.centroids = None
        self.weights = None
        self.random_state = random_state
        # Set random seed for reproducibility
        np.random.seed(random_state)

    def calculate_entropy(self, data_points, neighborhood_size=5):
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

    def set_weights(self, weights):
        """Set the weights to use for clustering (e.g., capacitance values)"""
        # Convert to numpy array with higher precision
        self.weights = np.array(weights, dtype=np.float64)
        
        # Check for zero or negative weights
        if np.any(self.weights <= 0):
            print("Warning: Found zero or negative weights. Converting to small positive values.")
            # Replace zero or negative values with a small positive value
            self.weights[self.weights <= 0] = np.min(self.weights[self.weights > 0]) * 0.1
        
        # Normalize weights to sum to 1 with higher precision
        weight_sum = np.sum(self.weights)
        self.weights = self.weights / weight_sum

    def fit(self, data_points, neighborhood_size=5):
        """Fit the model to the data points"""
        n_points = data_points.shape[0]
        n_features = data_points.shape[1]
        
        # Ensure weights are set
        if self.weights is None:
            raise ValueError("Weights must be set before fitting. Use set_weights() method.")
        
        # Calculate entropies with the specified neighborhood size
        entropies = self.calculate_entropy(data_points, neighborhood_size)
        
        # Combine weights with entropies
        # Higher entropy means more uncertainty, so we give those points more influence
        combined_weights = self.weights * (1 + entropies)
        combined_weights = combined_weights / np.sum(combined_weights)  # Normalize
        
        # Initialize centroids randomly within the data bounds
        min_vals = np.amin(data_points, axis=0)
        max_vals = np.amax(data_points, axis=0)
        self.centroids = np.random.uniform(min_vals, max_vals, size=(self.k, n_features))
        
        # Initialize labels
        labels = np.zeros(n_points, dtype=int)
        
        for _ in range(self.max_iterations):
            old_labels = labels.copy()
            
            # Assign points to clusters
            for i in range(n_points):
                distances = np.linalg.norm(data_points[i] - self.centroids, axis=1)
                weighted_distances = distances * combined_weights[i]
                labels[i] = np.argmin(weighted_distances)
            
            # Update centroids
            for j in range(self.k):
                if np.sum(labels == j) > 0:
                    cluster_points = data_points[labels == j]
                    cluster_weights = combined_weights[labels == j]
                    weighted_sum = np.sum(cluster_points * cluster_weights[:, np.newaxis], axis=0)
                    weight_sum = np.sum(cluster_weights)
                    self.centroids[j] = weighted_sum / weight_sum
            
            # Check for convergence
            if np.array_equal(old_labels, labels):
                break
        
        return labels 