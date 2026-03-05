# Clustering Audio Frames

Mach can group similar audio frames into clusters, useful for identifying repeated patterns, choruses, or distinct sections within a recording.

## Algorithms

### K-Means
Partition frames into K groups by minimizing within-cluster variance.

```python
from bird_mach.clustering import cluster_kmeans
result = cluster_kmeans(feature_matrix, n_clusters=5)
print(result.label_counts)
```

### DBSCAN
Density-based clustering — automatically finds the number of clusters and labels outliers as noise (-1).

```python
from bird_mach.clustering import cluster_dbscan
result = cluster_dbscan(feature_matrix, eps=0.5, min_samples=5)
```

## Workflow

1. Extract features (log-mel, MFCC, etc.)
2. Optionally reduce dimensions with UMAP
3. Cluster the resulting vectors
4. Color your visualization by cluster label
