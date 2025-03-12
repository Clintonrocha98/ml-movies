import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans
from scipy.sparse import hstack, csr_matrix
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import numpy as np

movies = pd.read_csv('preprocessed_data.csv')

movies['tag'] = movies['tag'].fillna('')

genres = movies['genres'].str.get_dummies(sep='|')

tfidf = TfidfVectorizer(stop_words='english', max_features=5000)
tag_features = tfidf.fit_transform(movies['tag'])

svd = TruncatedSVD(n_components=100, random_state=42)
tag_features_reduced = svd.fit_transform(tag_features)

# Use tag_features_reduced caso queira clusterizar usando tag
# Use csr_matrix(genres.values) caso queira clusterizar usando o genero

# Caso queira analisar com mais de uma feature, use o hstack
# features = hstack([csr_matrix(genres.values),tag_features_reduced])

# Caso queira somente usando somente um campo:
features = csr_matrix(genres.values)

kmeans = KMeans(n_clusters=3, random_state=42)

cluster_labels = kmeans.fit_predict(features)

movies['cluster'] = cluster_labels

# movies.to_csv('movies_with_clusters.csv', index=False)

# def recommend_movies(movie_title, n_recommendations=5):
#     if movie_title not in movies['title'].values:
#         return "Filme não encontrado ou não possui tags."
#     movie_cluster = movies[movies['title'] == movie_title]['cluster'].values[0]
#     recommendations = movies[movies['cluster'] == movie_cluster].sort_values(by=['genres','tag','rating'], ascending=False)
#     return recommendations.head(n_recommendations)

# print(recommend_movies('Toy Story'))

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

plt.show()