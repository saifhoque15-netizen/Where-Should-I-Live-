import streamlit as st
import base64
from components.header import render_header
from components.sidebar import render_sidebar
from components.background import add_bg
from pages import *

st.set_page_config(layout="wide")

def main():
    # --- Header ---
    render_header()

    # --- Sidebar ---
    render_sidebar()

    # --- Background ---
    add_bg("data-science-in-action\images\lisbon-wallpaper.jpg")
    st.write("""
     Welcome to Data Science in Action!
    We’ve taken our pre-processed data and turned it into fun, useful tools.
    Use the sidebar to explore everything — including our magical helper that suggests the city you’re clearly destined to live in, based on the criteria you care about.
    Pick your options, press a button, and let the data decide your future (don’t worry, it’s nicer than your uncle giving life advice).
    """)

    


if __name__ == "__main__":
    main()