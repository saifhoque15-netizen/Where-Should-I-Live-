import streamlit as st
from PIL import Image

APP_TITLE = "Where Should I Live 🏡"

def render_header():
    try:
        favicon = Image.open("data-science-in-action\images\house.png")
    except:
        favicon = None

    st.set_page_config(page_title=APP_TITLE, layout="wide", page_icon=favicon)
    st.title(APP_TITLE)