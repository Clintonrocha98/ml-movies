import pandas as pd
import re

movies = pd.read_csv('datasets/movies.csv')
ratings = pd.read_csv('datasets/ratings.csv')
tags = pd.read_csv('datasets/tags.csv')

tags['tag'] = tags['tag'].astype(str)
tags_grouped = tags.groupby('movieId')['tag'].apply(lambda x: ' '.join(x)).reset_index()

avg_ratings = ratings.groupby('movieId')['rating'].first().reset_index()

movies['year'] = movies['title'].apply(lambda x: re.search(r'\((\d{4})\)', x).group(1) if re.search(r'\((\d{4})\)', x) else None)
movies['title'] = movies['title'].apply(lambda x: re.sub(r'\(\d{4}\)', '', x).strip())
movies['year'] = pd.to_numeric(movies['year'], errors='coerce').fillna(0).astype(int)

movies_merged = movies.merge(avg_ratings, on='movieId', how='left') 
movies_merged = movies_merged.merge(tags_grouped, on='movieId', how='left') 

movies_merged['rating'] = movies_merged['rating'].fillna(0)
movies_merged['tag'] = movies_merged['tag'].fillna('')

movies_merged.to_csv('preprocessed_data.csv', index=False)

print("Junção concluída e salva em 'preprocessed_data.csv'.")