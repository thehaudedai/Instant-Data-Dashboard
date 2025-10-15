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
# Upload Files
uploaded_files = st.file_uploader(
    label="Upload Your Dataset", type=["csv", "xlsx"], accept_multiple_files=True
)
# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------
# View Files:
file_dict = {}

for file in uploaded_files:
    file_dict[file.name] = file

selected_file = st.selectbox(
    label="Select the DataFile to View", options=file_dict.keys(), index=None
)

if selected_file:
    file = file_dict[selected_file]

    if ".csv" in selected_file:
        df = pd.read_csv(file)
    elif ".xlsx" in selected_file:
        df = pd.read_excel(file)

    st.dataframe(df)
# ---------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------
# Saving dfs to Session State:
df_dict = {}

for key in file_dict:  # key is the filename (string)
    if key.endswith(".csv"):
        df_dict[key] = pd.read_csv(file_dict[key])
    elif key.endswith(".xlsx"):
        df_dict[key] = pd.read_excel(file_dict[key])
# ---------------------------------------------------------------------------------------------

for i in range(len(df_dict)):
    st.write(df_dict[i].key)
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
