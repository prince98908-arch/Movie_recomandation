# app.py
import gzip
import streamlit as st
import pandas as pd
import pickle
import requests

st.set_page_config(layout="wide")
st.title("Movie Recommendation System 🎬")


# Load precomputed similarity matrix
# Compressed pickle file ko load karne ka sahi tarika
with gzip.open("similarity_compressed_22mb.pkl", "rb") as f:
    similarity = pickle.load(f)

# Function to fetch movie poster from TMDB API
def fetch_poster(movie_id):
    api_key = "YOUR_TMDB_API_KEY"  # Replace with your TMDB API key
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    data = requests.get(url).json()
    if 'poster_path' in data and data['poster_path']:
        full_path = "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        return full_path
    else:
        return "https://via.placeholder.com/150"

# Recommendation function
def recommend(movie_name):
    movie_index = movies[movies['title'] == movie_name].index[0]
    distances = list(enumerate(similarity[movie_index]))
    movies_list = sorted(distances, reverse=True, key=lambda x: x[1])[1:6]  # top 5
    recommended_movies = []
    recommended_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_posters

# Movie selection
selected_movie = st.selectbox("Select a movie", movies['title'].values)

if st.button("Show Recommendations"):
    names, posters = recommend(selected_movie)
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        col.text(names[idx])
        col.image(posters[idx])
