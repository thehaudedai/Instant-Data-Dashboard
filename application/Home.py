import streamlit as st
import pandas as pd

# ---------------------------------------------------------------------------------------------

st.set_page_config(page_title="Home", page_icon="🏠")

st.title("Instant Data Dashboard")
st.text(
    "A Streamlit dashboard that lets users upload datasets, clean and explore data, and generate visualizations without coding."
)
# ---------------------------------------------------------------------------------------------
st.divider()

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
    label="Select A File to View the Data", options=st.session_state.df_dict.keys()
)

if selected_file:
    st.dataframe(st.session_state.df_dict[selected_file])
# ---------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
