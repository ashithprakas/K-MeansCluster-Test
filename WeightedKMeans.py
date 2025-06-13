import numpy as np
import matplotlib.pyplot as plt

class WeightedKMenasClustering:
    def __init__(self, k=3, max_iter=100):
        self.k = k
        self.max_iter = max_iter
        self.centroids = None

    @staticmethod
    def euclidean_distance(data_point, centroids):
        return np.sqrt(np.sum((centroids - data_point) ** 2, axis=1))

    def fit(self, data_points, weights=None):
        if weights is None:
            # If no weights provided, assume all equal weights
            weights = np.ones(data_points.shape[0])

        self.centroids = np.random.uniform(
            np.amin(data_points, axis=0),
            np.amax(data_points, axis=0),
            size=(self.k, data_points.shape[1])
        )

        for _ in range(self.max_iter):
            y = []

            # Assign each point to the closest centroid
            for data_point in data_points:
                distances = WeightedKMenasClustering.euclidean_distance(data_point, self.centroids)
                cluster_index = np.argmin(distances)
                y.append(cluster_index)

            y = np.array(y)

            cluster_indices = []
            for i in range(self.k):
                cluster_indices.append(np.argwhere(y == i))

            cluster_centers = []
            for i, indices in enumerate(cluster_indices):
                if len(indices) > 0:
                    # Extract points and their corresponding weights
                    points_in_cluster = data_points[indices[:, 0]]  # flatten indices
                    weights_in_cluster = weights[indices[:, 0]]

                    # Weighted average instead of simple mean
                    new_centroid = np.average(points_in_cluster, axis=0, weights=weights_in_cluster)
                    cluster_centers.append(new_centroid)
                else:
                    cluster_centers.append(self.centroids[i])

            cluster_centers = np.array(cluster_centers)

            # Check convergence
            if np.max(np.linalg.norm(self.centroids - cluster_centers, axis=1)) < 1e-4:
                break

            self.centroids = cluster_centers

        return y


# Example usage:
random_points = np.random.randint(0, 100, size=(100, 2))
weights = np.random.rand(100)  # some random weights between 0 and 1

kmeans = WeightedKMenasClustering(k=3)
labels = kmeans.fit(random_points, weights)

print("Centroids:", kmeans.centroids)
print("Labels:", labels)

plt.scatter(random_points[:, 0], random_points[:, 1], c=labels)
plt.scatter(kmeans.centroids[:, 0], kmeans.centroids[:, 1], c=range(len(kmeans.centroids)), marker='x', s=200)
plt.show()
