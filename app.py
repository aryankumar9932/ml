import streamlit as st
import pickle
import pandas as pd
import requests

# Your OMDb API Key
OMDB_API_KEY = "62403064"


# Function to fetch movie poster from OMDb
def fetch_poster(movie_title):
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if data.get("Response") == "True" and data.get("Poster") != "N/A":
            return data["Poster"]
        else:
            return "https://via.placeholder.com/300x450?text=No+Poster"
    except Exception:
        return "https://via.placeholder.com/300x450?text=No+Poster"


# Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        key=lambda x: x[1],
        reverse=True
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_title = movies.iloc[i[0]]["title"]
        recommended_movies.append(movie_title)
        recommended_posters.append(fetch_poster(movie_title))

    return recommended_movies, recommended_posters


# Load Movie Data
movies_dict = pickle.load(open("movies_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open("similarity.pkl", "rb"))

# Streamlit UI
st.title("🎬 Movie Recommender System")

selected_movie_name = st.selectbox(
    "Select a movie",
    movies["title"].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image(posters[0], use_container_width=True)
        st.write(names[0])

    with col2:
        st.image(posters[1], use_container_width=True)
        st.write(names[1])

    with col3:
        st.image(posters[2], use_container_width=True)
        st.write(names[2])

    with col4:
        st.image(posters[3], use_container_width=True)
        st.write(names[3])

    with col5:
        st.image(posters[4], use_container_width=True)
        st.write(names[4])
