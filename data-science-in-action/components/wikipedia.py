import streamlit as st
import wikipedia as wk
from time import time
import pandas as pd

def show_warning(message):
    st.warning(message)

def wiki_summary(url_or_title):
    try:
        # If you have a URL, extract the last part as the page title
        if url_or_title.startswith("http"):
            title = url_or_title.split("/")[-1].replace("_", " ")
        else:
            title = url_or_title
        
        summ = wk.summary(title, sentences=10)  # first 10 sentences
        summ = summ.replace("`", "")
        return summ
    except Exception as e:
        st.warning(f"Error retrieving summary: {str(e)}")
        return None

def wiki_images(url_or_title):
    try:
        if url_or_title.startswith("http"):
            title = url_or_title.split("/")[-1].replace("_", " ")
        else:
            title = url_or_title

        page = wk.page(title)
        img_urls = [img for img in page.images if img.lower().endswith(('.jpg', '.jpeg', '.png'))]
        return img_urls
    except Exception as e:
        st.warning(f"Error retrieving images: {str(e)}")
        return []