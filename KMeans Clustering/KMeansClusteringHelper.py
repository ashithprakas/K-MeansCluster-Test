import numpy as np

class KMenasClustering:
    def __init__(self, k=3, max_iter=100, random_state=42):
        self.k = k
        self.max_iter = max_iter
        self.centroids = None
        self.random_state = random_state
        np.random.seed(random_state)  # Set random seed for reproducibility

    @staticmethod
    def euclidean_distance(data_point,centroids): #Calculate the distance between a data point and all centroids and return an array of distances
        return np.sqrt(np.sum((centroids - data_point)**2, axis=1))
    
    def fit(self, date_points):
        # Convert input to numpy array if it's not already
        date_points = np.array(date_points)
        
        # Reset random seed before each fit to ensure same initial centroids
        np.random.seed(self.random_state)
        
        self.centroids = np.random.uniform(np.amin(date_points,axis=0),np.amax(date_points,axis=0),size=(self.k,date_points.shape[1])) #Set bounds for the initial centroids by using the min and max values of the data points

        for _ in range(self.max_iter):
            y = []

            for data_point in date_points:
                distances = KMenasClustering.euclidean_distance(data_point,self.centroids)
                cluster_index = np.argmin(distances) #Assign the data point to the cluster with the smallest distance
                y.append(cluster_index)

            y = np.array(y)

            cluster_indices = []
            for i in range(self.k):
                cluster_indices.append(np.argwhere(y==i)) #Find the indices of the data points that belong to each cluster

            cluster_centers = []
            for i , indices in enumerate(cluster_indices):
                if len(indices) > 0:
                    cluster_centers.append(np.mean(date_points[indices],axis=0)[0])
                else:
                    cluster_centers.append(self.centroids[i])

            if np.max(self.centroids - np.array(cluster_centers)) < 0.0001:
                break

            self.centroids = np.array(cluster_centers)

        return y




    
    
