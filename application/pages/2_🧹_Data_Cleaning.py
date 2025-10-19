import streamlit as st
import pandas as pd
import sys
import os

# ---------------------------------------------------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ---------------------------------------------------------------------------------------------
from components.sidebar import render_sidebar
from utils.summary import info_dtypes
from utils.manipulation import helper_change_column_name

# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------
st.set_page_config(page_title="Data Preprocessing", page_icon="🧹", layout="wide")
render_sidebar()

st.title("Data Preprocessing")
st.text("Clean and Edit the Data using any relevant methods you wish")
st.divider()
# ---------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------
# Checking Session State and Uploaded Data:
if not st.session_state.get("file_dict") or not st.session_state.get("df_dict"):
    st.warning("Please upload data first to start cleaning/processing.", icon="⚠️")
# ---------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------
# Select Dataframe:
if st.session_state.get("df_dict"):
    selected_file = st.selectbox(
        label="Select A File to Clean",
        options=st.session_state.df_dict.keys(),
        index=None,
    )
else:
    selected_file = st.selectbox(
        label="Select A File to Clean",
        options=[],
        index=None,
    )
st.session_state.selected_file = selected_file

if selected_file:
    selected_df = st.session_state.df_dict[selected_file]
else:
    selected_df = pd.DataFrame()
# ---------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------
# Column Operations
st.header("Column Operations:")

st.subheader("Rename Columns")
position = 1
col1, col2, col3 = st.columns(3)

for column in selected_df:
    if position == 1:
        with col1:
            new_column_name = st.text_input(
                label=f"Rename {column}",
                placeholder=column,
                label_visibility="collapsed",
                key=f"rename_{column}",
            )
        position = 2
    elif position == 2:
        with col2:
            new_column_name = st.text_input(
                label=f"Rename {column}",
                value=column,
                label_visibility="collapsed",
                key=f"rename_{column}",
            )
        position = 3
    elif position == 3:
        with col3:
            new_column_name = st.text_input(
                label=f"Rename {column}",
                value=column,
                label_visibility="collapsed",
                key=f"rename_{column}",
            )
        position = 1

rename_button = st.button(
    label="Rename Columns",
    use_container_width=True,
    type="secondary",
    on_click=helper_change_column_name,
)

if selected_file:
    selected_df = st.session_state.df_dict[selected_file]
# ---------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
