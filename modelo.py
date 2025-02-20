import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans
from scipy.sparse import hstack, csr_matrix
import numpy as np

movies = pd.read_csv('datasets/movies.csv')
ratings = pd.read_csv('datasets/ratings.csv')
tags = pd.read_csv('datasets/tags.csv')

movies['year'] = movies['title'].apply(lambda x: re.search(r'\((\d{4})\)', x).group(1) if re.search(r'\((\d{4})\)', x) else None)
movies['title'] = movies['title'].apply(lambda x: re.sub(r'\(\d{4}\)', '', x).strip())

movies['year'] = pd.to_numeric(movies['year'], errors='coerce') 

genres = movies['genres'].str.get_dummies(sep='|')

tags['tag'] = tags['tag'].astype(str) 
tags_grouped = tags.groupby('movieId')['tag'].apply(lambda x: ' '.join(x)).reset_index()

tfidf = TfidfVectorizer(stop_words='english', max_features=5000) 
tag_features = tfidf.fit_transform(tags_grouped['tag'])

svd = TruncatedSVD(n_components=100, random_state=42) 
tag_features_reduced = svd.fit_transform(tag_features)

avg_ratings = ratings.groupby('movieId')['rating'].mean().reset_index()

movies = movies.merge(avg_ratings, on='movieId', how='left')
movies = movies.merge(tags_grouped, on='movieId', how='left')

movies['rating'] = movies['rating'].fillna(0)  
movies['tag'] = movies['tag'].fillna('') 
movies['year'] = movies['year'].fillna(0)  

movies_with_tags = movies[movies['movieId'].isin(tags_grouped['movieId'])]
genres_with_tags = genres[movies['movieId'].isin(tags_grouped['movieId'])]

year_rating_sparse = csr_matrix(movies_with_tags[['year', 'rating']].astype(float).values)

features = hstack([csr_matrix(genres_with_tags.values), tag_features_reduced, year_rating_sparse])

kmeans = KMeans(n_clusters=10, random_state=42)
movies_with_tags['cluster'] = kmeans.fit_predict(features)

def recommend_movies(movie_title, n_recommendations=5):
    if movie_title not in movies_with_tags['title'].values:
        return "Filme não encontrado ou não possui tags."
    movie_cluster = movies_with_tags[movies_with_tags['title'] == movie_title]['cluster'].values[0]
    recommendations = movies_with_tags[movies_with_tags['cluster'] == movie_cluster].sort_values(by='rating', ascending=False)
    return recommendations.head(n_recommendations)

print(recommend_movies('Toy Story'))