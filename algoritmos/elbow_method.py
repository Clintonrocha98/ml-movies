import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans
from scipy.sparse import csr_matrix
import matplotlib.pyplot as plt

movies = pd.read_csv('preprocessed_data.csv')

movies['tag'] = movies['tag'].fillna('')

genres = movies['genres'].str.get_dummies(sep='|')

tfidf = TfidfVectorizer(stop_words='english', max_features=5000)
tag_features = tfidf.fit_transform(movies['tag'])

svd = TruncatedSVD(n_components=100, random_state=42)
tag_features_reduced = svd.fit_transform(tag_features)

features = csr_matrix(genres.values)

inertias = []
k_values = range(2, 15)

for k in k_values:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(features)
    inertias.append(kmeans.inertia_)

plt.figure(figsize=(10, 6))
plt.plot(k_values, inertias, 'bo-', markersize=8)
plt.xlabel('Número de Clusters (k)')
plt.ylabel('Inércia')
plt.title('Método do Cotovelo')
plt.savefig('metodo_cotovelo_k_values.png')  
plt.close() 