import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import pydeck as pdk
from components.background import add_bg

from components.matching import find_matching

favicon = Image.open("data-science-in-action/images/house.png")
st.set_page_config(page_title="City Recommendation", layout="wide", page_icon=favicon)

st.markdown(
    """
    <h1 style='
        background-color: lightblue;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    '>European City Recommendation 🌅</h1>
    """, 
    unsafe_allow_html=True
)

# --- Load data ---
@st.cache_data
def load_data():
    return pd.read_csv("data/city_data_with_coordinates.csv")

df = load_data()

# --- Sidebar ---

languages_available = ["Any"] + list(df['Main Spoken Languages'].str.split(',').explode().str.strip().unique())
lang_pref = st.sidebar.selectbox(
        'Prefered Main Spoken Language',
        languages_available)

w_salary = st.sidebar.number_input(
        "Min Monthly Salary (€)",
        min_value=0,
        max_value=20000,
        value=3000,
        step = 500)
    
w_unemployment = st.sidebar.slider("Unemployment Rate", min(df['Unemployment Rate']), max(df['Unemployment Rate']), np.mean(df['Unemployment Rate']))

w_gdp = st.sidebar.slider(
    "Max GDP per Capita (€)",
    int(df["GDP per Capita"].min()),
    int(df["GDP per Capita"].max()),
    int(df["GDP per Capita"].mean()),
    step=1000
)


w_rent = st.sidebar.slider(
    "Max Rent Price",
    min_value=int(df['Average Rent Price'].min()),
    max_value=int(df['Average Rent Price'].max()),
    value=int(df['Average Rent Price'].mean()),
    step=50
)

w_cost = st.sidebar.slider(
    "Max Cost of Living",
    min_value=int(df['Average Cost of Living'].min()),
    max_value=int(df['Average Cost of Living'].max()),
    value=int(df['Average Cost of Living'].mean()),
    step=50
)

run_button = st.sidebar.button("Find Matching Cities", type="primary")
results_placeholder = st.empty()

# --- Page ---
if run_button:
    preferences = {
        "Unemployment Rate": w_unemployment,
        "GDP per Capita": w_gdp,
        "Average Monthly Salary": w_salary,
        "Average Rent Price": w_rent,
        "Average Cost of Living": w_cost
    }

    matching_cities = find_matching(df, user_language=lang_pref, pref=preferences)

    if matching_cities.empty:
        st.toast("No match found! Try changing your preferences", icon="😪")
    else:
        st.balloons()
        st.markdown(f"<h3 style='text-align:center'>We suggest you:", unsafe_allow_html=True)

         # --- Youtube Video ---
        query = matching_cities['City'].iloc[0].replace(" ", "+") + "+city+tour"

        st.markdown(
            f"""
            <div style='text-align:center; background-color:lightgreen; padding:10px; border-radius:10px;'>
                <h1>{matching_cities['City'].iloc[0]}</h1>
                <a href='https://www.youtube.com/results?search_query={query}' target='_blank' 
                style='color:blue; text-decoration:underline; font-size:18px;'>
                Watch a city tour on YouTube
                </a>
            </div>
            """,
            unsafe_allow_html=True
            )

        # --- Other Cities ---
        st.divider()
        other_cities = matching_cities  # or skip top city with .iloc[1:]
        num_cols = 3
        cols = st.columns(num_cols)

        for i, (_, city) in enumerate(matching_cities.iterrows()):
            with cols[i % num_cols]:
                st.markdown(
                    f"""
                    <div style='
                        background-color:#f0f2f6; 
                        padding:20px; 
                        border-radius:15px; 
                        text-align:center; 
                        box-shadow: 2px 2px 10px rgba(0,0,0,0.1); 
                        margin-bottom:20px;
                        position:relative;
                    '>
                        <div style='
                            position:absolute; 
                            top:10px; 
                            right:10px; 
                            background-color:#ffcc00; 
                            border-radius:50%; 
                            width:30px; 
                            height:30px; 
                            display:flex; 
                            align-items:center; 
                            justify-content:center; 
                            font-weight:bold;
                        '>{i+1}</div>
                        <h3>{city['City']}</h3>
                        <p>Salary: €{city['Average Monthly Salary']}</p>
                        <p>Rent: €{city['Average Rent Price']}</p>
                        <p>Cost of Living: €{city['Average Cost of Living']}</p>
                        <p>Unemployment: {city['Unemployment Rate']}%</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


        # --- Location of the matching cities on the map ---
        st.divider()
        st.markdown(f"<h3 style='text-align:center'>Better to see them on the map:", unsafe_allow_html=True)

        map_df = df[df['City'].isin(matching_cities['City'])]
        map_df = map_df.rename(columns={"Latitude": "lat", "Longitude": "lon"})

        layer = pdk.Layer(
            "ScatterplotLayer",
            data=map_df,
            get_position='[lon, lat]',
            get_radius=25000,
            get_color=[255, 0, 0],
            pickable=True
        )

        tooltip = {"text": "{City}"}

        view_state = pdk.ViewState(
            longitude=map_df['lon'].mean(),
            latitude=map_df['lat'].mean(),
            zoom=3
        )

        st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip=tooltip))
        st.divider()


    