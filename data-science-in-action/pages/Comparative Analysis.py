import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
from components.flag import *
import pydeck as pdk
from components.highlighter import highlight_better_row, air_pollution
from components.wikipedia import wiki_summary, wiki_images


favicon = Image.open("data-science-in-action/images/house.png")
st.set_page_config(page_title="City Comparison", layout="wide", page_icon=favicon)

# --- Load data ---
@st.cache_data
def load_data(url):
    return pd.read_csv(url)

pds_url = "data/city_data_with_coordinates.csv"
df = load_data(pds_url)

env_url = "data/environment.csv"
env = load_data(env_url)
env = env.astype({
    "CO2 Emissions (per capita)" : "int8",
    "Pollution Index" : "int8",
    "Air Quality Index" : "int8",
    "Green Space Index" : "int8"
})

health_url = "data/health.csv"
health = load_data(health_url)
health = health.astype({
    "Health Care Index" : "int8",
    "Life Expectancy (Years)" : "int8"
})

tra_url = "data/transportation.csv"
tra = load_data(tra_url)
tra = tra.astype({
    "Traffic Index" : "int8",
    "Public Transport Satisfaction" : "int8"
})
# --- Sidebar ---
cities_available = list(df['City'].unique())
left_index = cities_available.index('Lisbon') if 'Lisbon' in cities_available else 0
right_index = cities_available.index('Milan') if 'Milan' in cities_available else 0

left_city = st.sidebar.selectbox(
    'City 1',
    cities_available,
    index = left_index
)

right_city = st.sidebar.selectbox(
    'City 2',
    cities_available,
    index = right_index
)
st.sidebar.divider()
st.sidebar.markdown("""
    This tool provides a side-by-side analysis of two cities using the city_data.csv plus available 
    data on demographics, crime rates, real estate trends, and more. Enter the name of the cities you want to compare 
    in the sidebar.
""")
if left_city == right_city:
    st.toast("Please select two different cities.", icon="🚫")
elif left_city is None or right_city is None:
    st.toast("Please select another city to compare.", icon="🚫")
else:
    # Start comparing
    col1, col2, col3 = st.columns(3)
    left_country = df[df['City'] == left_city]['Country'].iloc[0]
    right_country = df[df['City'] == right_city]['Country'].iloc[0]

    with col1:
        st.subheader(left_city)
        st.image(flag_from_country(left_country))
    with col2:
        st.subheader("Versus")
        st.header("🤔")
    with col3:
        st.subheader(right_city)
        st.image(flag_from_country(right_country))

    st.divider()

    # --- cost of Living ----
    st.subheader("Key Financials 💸")
    financial_columns = [
        "Average Monthly Salary",
        "Average Rent Price",
        "Average Cost of Living"
    ]

    financial_index = {
        "Average Monthly Salary": "Average Monthly Salary (€)",
        "Average Rent Price": "Average Rent Price (€)",
        "Average Cost of Living": "Average Cost of Living (€)"
    }

    left_data = df[df['City'] == left_city].iloc[0]
    right_data = df[df['City'] == right_city].iloc[0]

    financial_comparison_df = pd.DataFrame({
        left_city: left_data[financial_columns],
        right_city: right_data[financial_columns]
    })

    financial_comparison_df = financial_comparison_df.rename(index=financial_index)
    
    styled_df = financial_comparison_df.style.apply(highlight_better_row, axis=1)
    st.table(styled_df)

    # --- Demographics ---
    st.subheader('Demographics 👩‍🦳')

    demo_columns = [
        'Population Density', 'Population', 'Working Age Population',
        'Youth Dependency Ratio', 'Unemployment Rate', 'GDP per Capita']

    demo_comparison_df = pd.DataFrame({
        left_city: left_data[demo_columns],
        right_city: right_data[demo_columns]
    })

    row_name_map = {
        'Population Density': 'Population Density (People/sq. km)',
        'Population': 'Population (Count)',
        'Working Age Population': 'Working Age Population (Count)',
        'Youth Dependency Ratio': 'Youth Dependency Ratio (%)',
        'Unemployment Rate': 'Unemployment Rate (%)',
        'GDP per Capita': 'GDP per Capita (€)'
    }

    df_to_style = demo_comparison_df.rename(index=row_name_map)

    rows_no_decimals = [
        'Population Density (People/sq. km)', 
        'Population (Count)', 
        'Working Age Population (Count)'
    ]
    rows_percent = [
        'Youth Dependency Ratio (%)', 
        'Unemployment Rate (%)'
    ]
    rows_currency = [
        'GDP per Capita (€)'
    ]

    idx = pd.IndexSlice 

    styled_df = df_to_style.style\
        .apply(highlight_better_row, axis=1)\
        .format('{:,.0f}', subset=idx[rows_no_decimals, :])\
        .format('{:.1f}%', subset=idx[rows_percent, :])\
        .format('€{:,.0f}', subset=idx[rows_currency, :])

    st.table(styled_df)

    # --- Health Care ----
    st.subheader("Health Care 💊")
    health.drop('Country', axis=1, inplace=True)
    health_comparison_df = (
        health[health["City"].isin([right_city, left_city])]
        .set_index("City")
        .reindex([left_city, right_city])
        .T
    )

    styled_health = health_comparison_df.style.apply(highlight_better_row, axis=1)
    st.table(styled_health)

    # --- Transportation
    st.subheader("Transportation 🚡")
    tra.drop('Country', axis=1, inplace=True)
    tra_comparison_df = (
        tra[tra["City"].isin([left_city, right_city])]
        .set_index("City")
        .reindex([left_city, right_city])
        .T
    )

    styled_tra = tra_comparison_df.style.apply(highlight_better_row, axis=1)
    st.table(styled_tra)

    # --- Environment ---
    st.subheader("Environment 🌱")
    env.drop('Country', axis=1, inplace=True)
    env_comparison_df = (
        env[env["City"].isin([left_city, right_city])]
        .set_index("City")
        .reindex([left_city, right_city])
        .T
    )

    styled_env = env_comparison_df.style.apply(highlight_better_row, axis=1)
    st.table(styled_env)

    
    # --- Interactive Map of the Two Cities
    map_df = df[df['City'].isin([left_city, right_city])]
    map_df = map_df.rename(columns={"Latitude": "lat", "Longitude": "lon"})

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_df,
        get_position='[lon, lat]',
        get_radius=25000,
        get_color=[255, 0, 0],  # red markers
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

    # --- City Images
    left_city_images = wiki_images(left_data.get('Wikipedia_URL', '')) or []
    right_city_images = wiki_images(right_data.get('Wikipedia_URL', '')) or []

    max_images = 3
    left_city_images = left_city_images[:max_images]
    right_city_images = right_city_images[:max_images]


    # Display side by side
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(left_data['City'])
        for img in left_city_images:
            st.image(img, width=True)
        st.divider()
        st.write(wiki_summary(left_data['Wikipedia_URL']))

    with col2:
        st.subheader(right_data['City'])
        for img in right_city_images:
            st.image(img, width=True)
        st.divider()
        st.write(wiki_summary(right_data['Wikipedia_URL']))





