import streamlit as st
import pickle
import numpy as np
import requests

movies_titles = None
similarity = None
###Loading movies.pkl and similarity.pkl
# Verify file content
try:
    with open(r'movies.pkl', 'rb') as file:
        movies_list = pickle.load(file)
        movies_titles = movies_list['title'].values
    print("Movies pickle file loaded successfully.")
except pickle.UnpicklingError:
    print("Error: The Movie file is not a valid pickle file or is corrupted.")
# movies_list = pickle.load(open('movies.pkl', 'rb'))
# movies_titles = movies_list['title'].values
# similarity = pickle.load(open('similarity.pkl', 'rb'))
try:
    with open(r'similarity.pkl', 'rb') as file:
        similarity = pickle.load(file)
    print("Similarity pickle file loaded successfully.")
except pickle.UnpicklingError:
    print("Error: The Similarity file is not a valid pickle file or is corrupted.")

###fetching the movie poster
def fetch_poster(movie_id):
    headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1NDhkYTk4ZWEzZWYzNjA4NzhmYzYzM2U0NmQ2ZTEyOSIsIm5iZiI6MTcyOTI3NDg3NC4yMjY4NzcsInN1YiI6IjY3MTJhMjZlOGU4NDQ2NTdiN2ZiM2VlZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Xad3I4yt4FBOi3RrJCv3-m9McfHT2oe6ovTBYQoKsxQ"
    }
    response = requests.get('https://api.themoviedb.org/3/movie/{}?language=en-US'.format(movie_id), headers=headers)
    return "https://image.tmdb.org/t/p/w500/"+ response.json()['poster_path']

###Function to recommend movies
def recommended_movies(movie):
    try:
        # Find the index of the selected movie
        movie_index = np.nonzero(movies_titles == movie)[0][0]
        
        # Get the similarity scores for the selected movie
        distances = similarity[movie_index]
        
        # Get the top 5 recommended movies
        recommended_movies_list = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]
        
        # Initialize lists to store movie names and poster URLs
        movie_names = []
        poster_urls = []
        
        # Fetch the movie names and poster URLs for the recommended movies
        for i in recommended_movies_list:
            movie_id = movies_list.iloc[i[0]].movie_id
            movie_names.append(movies_list.iloc[i[0]].title)
            poster_urls.append(fetch_poster(movie_id))
        
        return movie_names, poster_urls
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return [], []

###Streamlit for UI work
st.title('Movie Recommendation System')

selected_movie = st.selectbox('Select a movie:', movies_titles)

if st.button('Recommend'):
    st.write('Here are some recommended movies you would also like:')
    movie_names, poster_urls = recommended_movies(selected_movie)

    cols = st.columns(5)

    for i, col in enumerate(cols):
        with col:
            st.header(movie_names[i])
            st.image(poster_urls[i])