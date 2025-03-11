import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans
from scipy.sparse import hstack, csr_matrix

movies = pd.read_csv('preprocessed_data.csv')

movies['tag'] = movies['tag'].fillna('')

genres = movies['genres'].str.get_dummies(sep='|')

tfidf = TfidfVectorizer(stop_words='english', max_features=5000)
tag_features = tfidf.fit_transform(movies['tag'])


svd = TruncatedSVD(n_components=100, random_state=42)
tag_features_reduced = svd.fit_transform(tag_features)

year_rating_sparse = csr_matrix(movies[['year', 'rating']].astype(float).values)

features = hstack([csr_matrix(genres.values), tag_features_reduced, year_rating_sparse])

n_clusters = 10
kmeans = KMeans(n_clusters=n_clusters, random_state=42)

cluster_labels = kmeans.fit_predict(features)

movies['cluster'] = cluster_labels

# movies.to_csv('movies_with_clusters.csv', index=False)


def recommend_movies(movie_title, n_recommendations=5):
    if movie_title not in movies['title'].values:
        return "Filme não encontrado ou não possui tags."
    movie_cluster = movies[movies['title'] == movie_title]['cluster'].values[0]
    recommendations = movies[movies['cluster'] == movie_cluster].sort_values(by=['genres','tag','rating'], ascending=False)
    return recommendations.head(n_recommendations)

print(recommend_movies('Toy Story'))