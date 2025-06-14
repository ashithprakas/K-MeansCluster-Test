import numpy as np

class WeightedKMeansClustering:
    def __init__(self, k=3, max_iterations=100, random_state=42):
        self.k = k
        self.max_iterations = max_iterations
        self.centroids = None
        self.weights = None
        self.random_state = random_state
        # Set random seed for reproducibility
        np.random.seed(random_state)

    def initialize_weights(self, n_points):
        # Initialize weights randomly between 0.1 and 1.0
        self.weights = np.random.uniform(0.1, 1.0, n_points)
        # Normalize weights
        self.weights = self.weights / np.sum(self.weights)

    def fit(self, data_points):
        n_points = data_points.shape[0]
        n_features = data_points.shape[1]
        
        # Initialize weights if not already done
        if self.weights is None:
            self.initialize_weights(n_points)
        
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
                weighted_distances = distances * self.weights[i]
                labels[i] = np.argmin(weighted_distances)
            
            # Update centroids
            for j in range(self.k):
                if np.sum(labels == j) > 0:
                    cluster_points = data_points[labels == j]
                    cluster_weights = self.weights[labels == j]
                    weighted_sum = np.sum(cluster_points * cluster_weights[:, np.newaxis], axis=0)
                    weight_sum = np.sum(cluster_weights)
                    self.centroids[j] = weighted_sum / weight_sum
            
            # Check for convergence
            if np.array_equal(old_labels, labels):
                break
        
        return labels 