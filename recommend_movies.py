import pandas as pd

movies = pd.read_csv('movies_with_clusters.csv')

def recommend_movies(movie_title, n_recommendations=10):
    if movie_title not in movies['title'].values:
        return "Filme não encontrado ou não possui tags."
    
    movie_cluster = movies[movies['title'] == movie_title]['cluster'].values[0]
    
    cluster_movies = movies[(movies['cluster'] == movie_cluster) & (movies['title'] != movie_title)]
    
    recommendations = cluster_movies.sort_values(by=['rating', 'genres', 'tag'], ascending=[False, False, False])
    
    return recommendations.head(n_recommendations)

print(recommend_movies('Toy Story'))