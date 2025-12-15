import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
from components.preferences import build_user_vector, build_city_matrix, normalize, recommend_cities

# --- Page Config and Favicon---
favicon = Image.open("data-science-in-action/images/house.png")
st.set_page_config(page_title="City Comparison", layout="wide", page_icon=favicon)

# --- Header ---
st.markdown(
    """
    <h1 style='
        background-color: lightblue;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    '>Find Your Ideal European City 🌍</h1>
    """, 
    unsafe_allow_html=True
)

# --- Session State ---
if "answers" not in st.session_state:
    st.session_state.answers = {}

# --- Load and Merge Data ---
@st.cache_data
def load_data(url):
    return pd.read_csv(url)

cities_df = load_data("data/city_data_with_coordinates.csv")
health_df = load_data("data/health.csv")
env_df = load_data("data/environment.csv")

cities_df = cities_df.merge(health_df, on=['City', 'Country'])
cities_df = cities_df.merge(env_df, on=['City', 'Country'])

# --- Build City Vector + Normalization Matrix ---
city_vectors = build_city_matrix(cities_df)
city_vectors_norm = normalize(city_vectors)


# --- Sidebar Inputs ---
with st.sidebar:    
    with st.form("lifestyle_form"):
        q1 = st.radio(
            "Your perfect Saturday looks like:",
            ["Hiking or being in nature", "Cafés, museums, slow walks", "Bars, clubs, and nightlife"]
        )

        q2 = st.radio(
            "Your ideal home is:",
            ["Small but central", "Spacious and quiet", "Flexible, I adapt easily"]
        )

        q3 = st.radio(
            "You meet people mostly through:",
            ["Work and professional networks", "Community events and hobbies", "Expat or international circles"]
        )

        q4 = st.radio(
            "Your daily rhythm is:",
            ["Early mornings", "Balanced schedule", "Late nights"]
        )

        q5 = st.slider("Stability vs Adventure", 0, 10, 5)

        submitted = st.form_submit_button("Find my City")

# --- Main Logic ---
if submitted:
    st.session_state.answers = {
        "weekend": q1, "home": q2, "social": q3, 
        "rhythm": q4, "adventure": q5
    }

    user_vec = build_user_vector(st.session_state.answers)
    
    top_cities, top_scores = recommend_cities(user_vec, city_vectors_norm, top_n=3)
    
    st.subheader(f"Top {len(top_cities)} Recommendations")
    
    cols = st.columns(len(top_cities))
    
    medals = ["🥇", "🥈", "🥉"]
    colors = ["#FFD700", "#C0C0C0", "#CD7F32"]

    for i, city in enumerate(top_cities):
        # Handle cases where Wikipedia_URL might be missing or different
        try:
            url = cities_df.loc[cities_df["City"] == city, "Wikipedia_URL"].values[0]
        except:
            url = f"https://en.wikipedia.org/wiki/{city}"

        with cols[i]:
            st.markdown(f"""
            <div style='
                background-color: {colors[i] if i < 3 else "white"};
                padding: 20px;
                border-radius: 10px;
                border: 1px solid #ddd;
                text-align: center;
                height: 200px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            '>
                <h3 style='margin:0;'>{medals[i]} {city}</h3>
                <p style='font-size: 1.2em; color: #555;'>Score: {top_scores[i]:.2f}</p>
                <a href="{url}" target="_blank" style="text-decoration:none; color: #0068c9; font-weight: bold;">Explore</a>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    # Optional: Debug expander to see why these cities were picked
    with st.expander("See algorithm details (Debug)"):
        st.write("User Vector:", user_vec)
        st.write("City Data (Normalized):")
        st.dataframe(city_vectors_norm.loc[top_cities])