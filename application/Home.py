import streamlit as st
import pandas as pd
import sys
import os

# ---------------------------------------------------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ---------------------------------------------------------------------------------------------
from utils.summary import (
    info_summary,
    info_duplicate_rows,
    info_shape,
    info_sample_rows,
)
from components.sidebar import render_sidebar

# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------
st.set_page_config(page_title="Home", page_icon="🏠", layout="wide")
render_sidebar()  # TODO: Edit Sidebar; No CSV in label, proper formatting.


st.title("Instant Data Dashboard")
st.text(
    "A Streamlit dashboard that lets users upload datasets, clean and explore data, and generate visualizations without coding."
)
# ---------------------------------------------------------------------------------------------
st.divider()
temp_file = "test_data\products.csv"
# ---------------------------------------------------------------------------------------------
# File Upload:
uploaded_files = st.file_uploader(
    label="Upload your Dataset(s)", type=["csv", "xlsx"], accept_multiple_files=True
)
# ---------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------
# Session State:
if "file_dict" not in st.session_state:
    st.session_state.file_dict = {}
if "df_dict" not in st.session_state:
    st.session_state.df_dict = {}
# ---------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------
if uploaded_files:
    for file in uploaded_files:
        filename = file.name

        st.session_state.file_dict[filename] = file

        if filename.endswith(".csv"):
            df = pd.read_csv(file)
        elif filename.endswith(".xlsx"):
            df = pd.read_excel(file)
        else:
            continue

        st.session_state.df_dict[filename] = df
# ---------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------
# Select File & View:
selected_file = st.selectbox(
    label="Select A File to View the Data",
    options=st.session_state.df_dict.keys(),
    index=None,
)

if selected_file:
    st.dataframe(st.session_state.df_dict[selected_file])

st.divider()
# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------
# Basic Info of the Selected File:
if selected_file:
    current_df = st.session_state.df_dict[selected_file]
    st.header("Info Of the Dataset")

    current_df_row, current_df_column = info_shape(current_df)
    st.write(f"Shape: {current_df_row} Rows x {current_df_column} Columns")

    summary_df = info_summary(current_df)
    st.table(summary_df)

    dupes_amount, dupes_df = info_duplicate_rows(current_df)
    if dupes_amount > 0:
        st.subheader("Duplicated Rows")
        st.info(
            "Only the duplicated rows are shown. The first occurrence of these rows are not shown!"
        )
        st.dataframe(dupes_df)

    st.divider()

    with st.expander(label="View the sample dataframe [First, Last or Random Rows]"):
        col1, col2 = st.columns(2)
        with col1:
            n_rows = st.select_slider(
                label="No. Rows to Display", options=[2, 3, 4, 5, 6, 7, 8]
            )
        with col2:
            sequence = st.selectbox(
                label="Select the Sequence", options=["Random", "Head", "Tail"]
            )

        if sequence == "Random":
            is_random = True
        else:
            is_random = False
        start_from = sequence

        st.table(
            info_sample_rows(
                df=current_df, number=n_rows, random=is_random, start=start_from
            )
        )
# ---------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
