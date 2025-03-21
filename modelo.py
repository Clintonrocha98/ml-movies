import pandas as pd
from sklearn.cluster import KMeans
from scipy.sparse import csr_matrix
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import numpy as np
from joblib import dump

movies = pd.read_csv('preprocessed_data.csv')

movies['tag'] = movies['tag'].fillna('')
genres = movies['genres'].str.get_dummies(sep='|')
features = csr_matrix(genres.values)

kmeans = KMeans(n_clusters=4, random_state=42)
cluster_labels = kmeans.fit_predict(features)
movies['cluster'] = cluster_labels

pca = PCA(n_components=2)
features_2d = pca.fit_transform(features.toarray())
cluster_centers_2d = pca.transform(kmeans.cluster_centers_)

unique_clusters = np.unique(cluster_labels)

plt.figure(figsize=(10, 6))

for cluster in unique_clusters:
    cluster_points = features_2d[cluster_labels == cluster] 
    plt.scatter(
        cluster_points[:, 0], 
        cluster_points[:, 1], 
        label=f'Cluster {cluster}', 
        alpha=0.6
    )

plt.scatter(
    cluster_centers_2d[:, 0], 
    cluster_centers_2d[:, 1], 
    c='red', 
    marker='X', 
    s=200, 
    label='Centros'
)

plt.legend()
plt.title('Visualização dos Clusters com PCA')

plt.savefig('clusters_pca.png', dpi=300, bbox_inches='tight') 
plt.close()

movies.to_csv('movies_with_clusters.csv', index=False)

dump(kmeans, 'movies_model.pkl')