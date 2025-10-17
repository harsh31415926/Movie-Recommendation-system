import streamlit as st
import pickle
import pandas as pd
import requests

# Load similarity matrix
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Load movie list
movie_list = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_list)

# Function to fetch poster from OMDb
def fetch_poster_omdb(movie_name):
    api_key = "5c55ec1f"  # replace with your API key
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={api_key}"
    data = requests.get(url).json()
    if data.get('Poster') and data['Poster'] != 'N/A':
        return data['Poster']
    else:
        return None

# Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:
        title = movies.iloc[i[0]].title
        recommended_movies.append(title)
        recommended_posters.append(fetch_poster_omdb(title))  # fetch poster for each recommended movie

    return recommended_movies, recommended_posters

# Streamlit UI
st.title('Movie Recommender System')
selected_movie_name = st.selectbox("Which movie's recommendation do you want?", movies['title'].values)

if st.button("Recommend"):
    rec_movies, rec_posters = recommend(selected_movie_name)

    # Create 5 columns for displaying movies
    c1, c2, c3, c4, c5 = st.columns(5)
    columns = [c1, c2, c3, c4, c5]

    for idx, col in enumerate(columns):
        col.markdown(f"<h4 style='text-align: center;'>{rec_movies[idx]}</h4>", unsafe_allow_html=True)
        col.image(rec_posters[idx])
