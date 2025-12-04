import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from components.background import add_bg

from components.matching import find_matching

favicon = Image.open("data-science-in-action\images\house.png")
st.set_page_config(page_title="City Recommendation", layout="wide", page_icon=favicon)
st.title("European City Recommendation System")

# --- Load data ---
@st.cache_data
def load_data():
    return pd.read_csv("data\city_data_clean.csv")

df = load_data()

# --- Streamlit UI ---
st.subheader("Set Your Preferences:")

# Row 1
col1, col2 = st.columns(2)

with col1:
    languages_available = ["Any"] + list(df['Main Spoken Languages'].str.split(',').explode().str.strip().unique())
    lang_pref = st.selectbox(
        'Prefered Main Spoken Language',
        languages_available
    )

with col2:
    w_salary = st.number_input(
        "Your Monthly Salary (€)",
        min_value=0,
        max_value=20000,
        value=3000,
        step = 500)
    
# Row 2
c1, c2, c3, c4 = st.columns(4)

with c1:
    w_unemployment = st.slider("Unemployment Rate", min(df['Unemployment Rate']), max(df['Unemployment Rate']), np.mean(df['Unemployment Rate']))

with c2:
    w_gdp = st.slider("GDP per Capita", 0, 10, 5)

with c3:
    w_rent = st.slider(
    "Average Rent Price",
    min_value=int(df['Average Rent Price'].min()),
    max_value=int(df['Average Rent Price'].max()),
    value=int(df['Average Rent Price'].mean()),
    step=50
)

with c4:
    w_cost = st.slider(
        "Average Cost of Living",
        min_value=int(df['Average Cost of Living'].min()),
        max_value=int(df['Average Cost of Living'].max()),
        value=int(df['Average Cost of Living'].mean()),
        step=50
)


run_button = st.button("Find Matching Cities", type="primary")

results_placeholder = st.empty()

if run_button:
    
    weights = {
        "Unemployment Rate": w_unemployment,
        "GDP per Capita": w_gdp,
        "Average Monthly Salary": w_salary,
        "Average Rent Price": w_rent,
        "Average Cost of Living": w_cost
    }

    matching_cities = find_matching(df, user_language=lang_pref, weights=weights)

    if matching_cities.empty:
        st.toast("No match found! try changing your preferences", icon="😪")
    else:
        st.balloons()
        max_size = 40
        min_size = 15
        n = len(matching_cities)

        for i, city in enumerate(matching_cities['City']):
            size = max_size - i * (max_size - min_size) / max(n - 1, 1)
            stars = "★" * (5 - i)  # 5 → 1 stars
            st.markdown(
                f"<p style='text-align:center; font-size:{size}px'>{city} {stars}</p>",
                unsafe_allow_html=True)


    