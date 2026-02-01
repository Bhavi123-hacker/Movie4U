import streamlit as st
import pickle
import pandas as pd

# Load data
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommendations = []

    for i in movies_list:
        recommendations.append({
            "title": movies.iloc[i[0]]['title'],
            "details": movies.iloc[i[0]]['tags'],   # FIXED
            "similarity": round(i[1], 3)
        })

    return recommendations

# Streamlit UI
st.title("🎬 Movie Recommendation System")

selected_movie_name = st.selectbox(
    "Select a movie",
    movies['title'].values
)

if st.button("Recommend"):
    results = recommend(selected_movie_name)

    st.subheader("Recommended Movies")

    for idx, movie in enumerate(results, start=1):
        st.markdown(f"### {idx}. {movie['title']}")
        st.write(f"🔗 **Similarity Score:** {movie['similarity']}")
        st.write(f"📝 **Details:** {movie['details']}")
        st.markdown("---")
