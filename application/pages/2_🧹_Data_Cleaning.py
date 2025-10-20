import streamlit as st
from streamlit_sortables import sort_items
import pandas as pd
import sys
import os

# ---------------------------------------------------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ---------------------------------------------------------------------------------------------
from components.sidebar import render_sidebar
from utils.summary import info_dtypes, info_sample_rows, info_duplicate_rows
from utils.manipulation import (
    helper_change_column_name,
    helper_drop_columns,
    helper_drop_duplicate_rows,
    helper_filter_dataset,
    helper_drop_displayed_rows,
)

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

st.divider()
# ---------------------------------------------------------------------------------------------


# Column Operations:
st.header("Column Operations:")
# ---------------------------------------------------------------------------------------------
# Rename Columns
st.subheader("Rename Columns")
position = 1
col1, col2, col3 = st.columns(3)

for column in selected_df:
    if position == 1:
        with col1:
            new_column_name = st.text_input(
                label=f"Rename {column}",
                value=column,
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
# Drop Columns:
st.subheader("Drop Columns")
st.write("Select the columns you wish to remove")
col1, col2 = st.columns([0.8, 0.2], vertical_alignment="center")

with col1:
    column_drop_list = st.pills(
        label="Select the columns you wish to remove",
        options=selected_df.columns,
        label_visibility="collapsed",
        selection_mode="multi",
        key="column_drop_list",
    )
with col2:
    st.button(
        label="Drop Columns",
        use_container_width=True,
        on_click=helper_drop_columns,
    )

if selected_file:
    selected_df = st.session_state.df_dict[selected_file]
# ---------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------
# Reorder Columns:
st.subheader("Reorder Columns")
sorted_columns = sort_items(items=selected_df.columns.to_list())

selected_df = selected_df[sorted_columns]
if selected_file:
    selected_df = st.session_state.df_dict[selected_file]
st.dataframe(info_sample_rows(selected_df, 3, random=False, start="Head"))

st.divider()
# ---------------------------------------------------------------------------------------------

# Column Operations:
st.header("Row Operations:")
# ---------------------------------------------------------------------------------------------
# Drop Duplicates
st.subheader("Drop Duplicate Rows")
duped_df = info_duplicate_rows(selected_df)[1]
if duped_df.empty:
    st.success("No Duplicate Rows")
else:
    st.dataframe(duped_df)
    col1, col2, col3 = st.columns(3)
    with col2:
        st.button(
            label="Drop Duplicate Rows",
            use_container_width=True,
            on_click=helper_drop_duplicate_rows,
        )

if selected_file:
    selected_df = st.session_state.df_dict[selected_file]
# ---------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------
# Drop Rows (By Condition + By Specific Row)
st.subheader("Drop Rows")

# Condition Based:
col1, col2, col3, col4 = st.columns([0.3, 0.15, 0.35, 0.2])
with col1:
    column_name = st.selectbox(
        label="Column Name",
        options=selected_df.columns,
        placeholder="Age",
        index=None,
        key="drop_row_column",
    )
with col2:
    operator = st.selectbox(
        label="Operator",
        options=["==", "!=", ">", ">=", "<", "<=", "Contains"],
        index=0,
        key="drop_row_operator",
    )
with col3:
    comparison_value = st.text_input(
        label="Value", placeholder="30", key="drop_row_value"
    )
with col4:
    comparison_value_type = st.selectbox(
        label="Value Type",
        options=["String", "Integer", "Float", "Boolean"],
        placeholder="Integer",
        key="drop_row_type",
    )
filter_button = st.button(
    label="Filter Dataset", use_container_width=True, on_click=helper_filter_dataset
)
if filter_button:
    if "drop_row_df" in st.session_state:
        if len(st.session_state.drop_row_df) == 0:
            st.info("No Rows matched the condition above!")
        else:
            st.dataframe(st.session_state.drop_row_df)
            st.button(
                f"Delete {len(st.session_state.drop_row_df)} Rows",
                on_click=helper_drop_displayed_rows,
                use_container_width=True,
            )

# TODO: Contains Error When not string (Column when not string)
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
