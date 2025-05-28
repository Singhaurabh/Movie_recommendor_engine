import streamlit as st
import pickle
import requests
import base64

# Replace this with your actual TMDb API key
API_KEY = '413ad00e6970f1aad1913283c5279ee2'  
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    data = response.json()
    poster_path = data.get("poster_path", "")
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        return "https://via.placeholder.com/150"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movie_names, recommended_movie_posters

def get_base64_encoded_image(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Load the image and encode
local_img_path = "template/cinematography-symbols-black-background.jpg"
encoded_img = get_base64_encoded_image(local_img_path)

# Custom CSS to remove top black patch and make widgets transparent
st.markdown(f"""
<style>
html, body, .stApp {{
    margin: 0;
    padding: 0;
    height: 100%;
    background-image: url("data:image/jpg;base64,{encoded_img}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

.stContainer {{
    background-color: rgba(0, 0, 0, 0.7);
    padding: 30px;
    border-radius: 15px;
    color: white;
    box-shadow: 0 4px 15px rgba(0,0,0,0.4);
    margin-top: 20px;
}}

header, footer {{
    visibility: hidden;
}}

section[data-testid="stSidebar"] {{
    background-color: transparent;
}}

div[data-testid="stSelectbox"] > div {{
    background-color: rgba(255, 255, 255, 0.1);
    color: white;
    border-radius: 10px;
}}

div[data-baseweb="select"] {{
    background-color: transparent !important;
}}

.stButton button {{
    background-color: #ff4b4b;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 8px 16px;
}}

.stButton button:hover {{
    background-color: #ff3333;
}}
</style>
""", unsafe_allow_html=True)

# Load pickled files
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Main content

st.header('🎬 Movie Recommender System')

movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

if st.button('Show Recommendation'):
    names, posters = recommend(selected_movie)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(posters[i])
            st.caption(names[i])

st.markdown('</div>', unsafe_allow_html=True)
