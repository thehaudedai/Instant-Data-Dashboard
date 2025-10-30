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
    helper_apply_dtype_and_rename,
    helper_create_column,
)

# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------
# Page Config
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
# Adding / Validating Column Config for every file
if f"column_config_{selected_file}" not in st.session_state:
    st.session_state[f"column_config_{selected_file}"] = {}

column_config = st.session_state.get(f"column_config_{selected_file}", {})
# ---------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------
# Main Data Editor Dataframe
st.data_editor(
    data=st.session_state.df_dict[selected_file],
    use_container_width=True,
    hide_index=False,
    num_rows="dynamic",
    key=f"data_edit_{selected_file}",
    column_config=column_config or None,
)

with st.expander("Changes & Edits"):
    st.write(st.session_state.get(f"data_edit_{selected_file}"))
# ---------------------------------------------------------------------------------------------


st.divider()
# ---------------------------------------------------------------------------------------------
# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "Column Management",
        "Missing Data Handling",
        "Transformation",
        "Reshaping & Aggregation",
        "Filtering",
        "Export",
    ]
)
# ---------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------
with tab1:
    # Column Operations:
    st.header("Column Operations:")

    # ---------------------------------------------------------------------------------------------
    # Change Data Type:
    st.subheader("Rename / Change Data Types")

    possible_data_types = [
        "int64",
        "float64",
        "boolean",
        "string",
        "object",
        "category",
        "datetime64[ns]",
        "timedelta64[ns]",
        "datetime64[ns, UTC]",
        "period[M]",
        "period[Q]",
        "Int64",
        "Float64",
        "complex128",
    ]

    dtype_df = pd.DataFrame(
        [
            {"Column Name": col, "DataType": info_dtypes(selected_df, col)}
            for col in selected_df
        ]
    )
    if not dtype_df.empty:
        dtype_df["DataType"] = dtype_df["DataType"].astype(str)

        dtype_df_column_config = {
            "Column Name": st.column_config.TextColumn("Column Name", disabled=False),
            "DataType": st.column_config.SelectboxColumn(
                "DataType",
                options=possible_data_types,
                required=True,
                help="Select a datatype for this column",
            ),
        }
    else:
        dtype_df_column_config = None

    st.data_editor(
        data=dtype_df,
        num_rows="fixed",
        column_config=dtype_df_column_config or None,
        key="dtype_editor",
    )

    if st.button("Apply Renames and DataType Changes", use_container_width=True):
        helper_apply_dtype_and_rename()

    st.divider()
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

    st.divider()
    # ---------------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------------
    # Reorder Columns:
    st.subheader("Reorder Columns")
    sorted_columns = sort_items(items=selected_df.columns.to_list())

    selected_df = selected_df[sorted_columns]
    if selected_file:
        st.session_state.df_dict[selected_file] = selected_df
    st.dataframe(info_sample_rows(selected_df, 3, random=False, start="Head"))

    st.divider()
    # ---------------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------------
    # Create Column (With Values)
    st.subheader("Create New Column")
    new_col_name = st.text_input(label="Column Name", placeholder="Name of the Column")

    st.button(label="Create Column", on_click=helper_create_column)

    st.divider()
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
# ---------------------------------------------------------------------------------------------
