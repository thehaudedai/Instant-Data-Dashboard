import streamlit as st
import pandas as pd
import sys
import os

# ---------------------------------------------------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ---------------------------------------------------------------------------------------------
from components.sidebar import render_sidebar

# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------
st.set_page_config(page_title="Data Preprocessing", page_icon="🧹", layout="wide")
render_sidebar()

st.title("Model Trainer")
st.text("Train Basic ML models on the go using the uploaded data")
st.divider()
# ---------------------------------------------------------------------------------------------
