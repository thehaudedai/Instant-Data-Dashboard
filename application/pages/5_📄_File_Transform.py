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

st.title("File Conversion")
st.text("Convert Files into suitable file types")
st.divider()
# ---------------------------------------------------------------------------------------------
