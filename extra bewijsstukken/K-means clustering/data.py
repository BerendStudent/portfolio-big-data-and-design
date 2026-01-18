import numpy as np
import matplotlib.pyplot as plt

dataset_location = 'opdrachten/K-means clustering/dataset1.csv' #Direct path, or it wouldn't work.

data = np.genfromtxt(dataset_location, delimiter=';', usecols=[1,2,3,4,5,6,7], converters={5: lambda s: 0 if s == b"-1" else float(s), 7: lambda s: 0 if s == b"-1" else float(s)})

dates = np.genfromtxt(dataset_location, delimiter=';', usecols=[0])
labels = []
for label in dates:
  if label < 20000301:
    labels.append('winter')
  elif 20000301 <= label < 20000601:
    labels.append('lente')
  elif 20000601 <= label < 20000901:
    labels.append('zomer')
  elif 20000901 <= label < 20001201:
    labels.append('herfst')
  else: # from 01-12 to end of year
    labels.append('winter')

def distance(a, b):
    return np.linalg.norm(a - b)

def calculate_centroid(cluster): 
    if len(cluster) == 0:
        return np.zeros_like(cluster[0])  # avoid crash on empty cluster
    return np.mean(cluster, axis=0)

def cluster(k, data):
    centroids = data[:k].copy()
    for _ in range(100):
        clusters = [[] for _ in range(k)]
        for point in data:
            distances = [distance(point, centroid) for centroid in centroids] #Finds distance between the point and a given cluster center
            cluster_index = np.argmin(distances)  #Finds the number of the cluster whose centroid is closest
            clusters[cluster_index].append(point) #adds the point to that cluster
        new_centroids = [calculate_centroid(cluster) for cluster in clusters] #Tries new clusters
        new_centroids = np.array(new_centroids)
        if np.allclose(new_centroids, centroids): #If the new cluster is really, really close to the old one, ignore it
            break
        centroids = new_centroids
    return clusters, centroids


def normalize_data(data):
    mean = np.mean(data, axis=0)
    std = np.std(data, axis=0)
    std[std == 0] = 1
    return (data - mean) / std

def sum_of_squares(clusters, centroids): #Works a bit like calculating the error, we want to minimise the distances involved.
    summed = 0
    for i, cluster in enumerate(clusters):
        for point in cluster:
            sumed += np.linalg.norm(point - centroids[i]) ** 2
    return summed

def scree_plot(data, max_k=10):
    sum_values = []
    k_range = range(1, max_k + 1)
    
    for k in k_range:
        clusters, centroids = cluster(k, data)
        summed = sum_of_squares(clusters, centroids)
        sum_values.append(summed)
    
    plt.plot(k_range, sum_values, marker='o')
    plt.xlabel('Number of clusters')
    plt.ylabel('Sum of squared distances')
    plt.title('K clusters')
    plt.xticks(k_range)
    plt.grid(True)
    plt.show()


normalized_data = normalize_data(data)
scree_plot(normalized_data)  # Uses full 7D data
