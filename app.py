import streamlit as st
import pickle
import joblib
import requests
import pandas as pd
from scipy import sparse   # IMPORTANT for sparse pkl

# =============================
# CONFIG
# =============================
st.set_page_config(page_title="Movie Recommender", layout="wide")

TMDB_API_KEY = "PUT_YOUR_TMDB_API_KEY_HERE"

# =============================
# LOAD FILES
# =============================
movies = pickle.load(open("movies.pkl", "rb"))
similarity = joblib.load("similarity_compressed_22mb.pkl")

# =============================
# FUNCTIONS
# =============================
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"
    data = requests.get(url).json()
    poster_path = data.get("poster_path")
    
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

def recommend(movie):
    index = movies[movies["title"] == movie].index[0]

    # Sparse matrix safe conversion
    if sparse.issparse(similarity):
        distances = similarity[index].toarray().flatten()
    else:
        distances = similarity[index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters

# =============================
# UI
# =============================
st.title("🎬 Movie Recommendation System")

selected_movie = st.selectbox(
    "Select a movie",
    movies["title"].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])

