import pandas as pd
import streamlit as st
import pickle
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=020b311fe0559698373a16008dc6a672&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for x in movies_list:
        movie_id = movies.iloc[x[0]].movie_id
        recommended_movies.append(movies.iloc[x[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# Load movie data and similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

# Initialize session state
if 'search_results' not in st.session_state:
    st.session_state.search_results = pd.DataFrame(columns=['Selected Movie', 'Recommended Movies'])

selected_movie_name = st.selectbox(
    'Select a movie:',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    st.write("## Recommended Movies")
    
    # Display recommended movies vertically
    col1, col2, col3, col4, col5 = st.columns(5)
    cols = [col1, col2, col3, col4, col5]
    
    for name, poster, col in zip(names, posters, cols):
        with col:
            st.text(name)
            st.image(poster, use_column_width=True)

    # Update search results
    new_result = pd.DataFrame({'Selected Movie': [selected_movie_name], 'Recommended Movies': [", ".join(names)]})
    st.session_state.search_results = st.session_state.search_results.append(new_result, ignore_index=True)

# Display all search results
st.write("## All Search Results")
st.table(st.session_state.search_results)
