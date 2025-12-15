import streamlit as st
import base64
from components.background import add_bg
from pages import *
from PIL import Image

st.set_page_config(layout="wide")

APP_TITLE = "Where Should I Live 🏡"

def render_header():
    try:
        favicon = Image.open("data-science-in-action/images/house.png")
        st.header("Bem-vindo ao Data Science in Action!")
    except:
        favicon = None

def render_sidebar():
    st.sidebar.markdown("""
     We’ve taken our pre-processed data and turned it into fun, useful tools.
    Use the sidebar to explore everything — including our magical helper that suggests the city you’re clearly destined to live in, based on the criteria you care about.
    Pick your options, press a button, and let the data decide your future (don’t worry, it’s nicer than your uncle giving life advice).
    """)
    st.divider()
    st.sidebar.markdown("""
            **GitHub Repository:**  
            [Where Should I Live](https://github.com/saifhoque15-netizen/where-should-I-live)
        """) 


def main():
    # --- Header ---
    render_header()

    # --- Sidebar ---
    render_sidebar()

    # --- Background ---
    add_bg("data-science-in-action/images/lisbon-wallpaper.jpg")
    

if __name__ == "__main__":
    main()