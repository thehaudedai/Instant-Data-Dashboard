import streamlit as st
from streamlit_sortables import sort_items
import pandas as pd
import datetime
import sys
import os

# ---------------------------------------------------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ---------------------------------------------------------------------------------------------
from components.sidebar import render_sidebar
from components.display import display_type_based_input, display_function_options
from utils.preset import DATA_TYPE_OPTIONS, FILL_OPTIONS
from utils.summary import (
    info_dtypes,
    info_sample_rows,
    info_duplicate_rows,
    info_filter_dataset,
)
from utils.manipulation import (
    helper_drop_columns,
    helper_apply_dtype_and_rename,
    helper_create_column,
    helper_drop_null_rows,
    helper_fill_null_values,
    helper_drop_duplicate_rows,
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
# -----------------------------------------------------------                ----------------------------------


# ---------------------------------------------------------------------------------------------
# Adding / Validating Column Config for every file
if f"column_config_{selected_file}" not in st.session_state:
    st.session_state[f"column_config_{selected_file}"] = {}

column_config = st.session_state.get(f"column_config_{selected_file}", {})
# ---------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------
# Main Data Editor Dataframe
primary_df_editor = st.data_editor(
    data=selected_df,
    use_container_width=True,
    hide_index=False,
    num_rows="dynamic",
    key=f"data_edit_{selected_file}",
    column_config=column_config or None,
)

with st.expander("Changes & Edits"):
    st.write(st.session_state.get(f"data_edit_{selected_file}"))

if st.button(label="Save Edits", use_container_width=True):
    st.session_state.df_dict[selected_file] = primary_df_editor

if selected_file:
    selected_df = st.session_state.df_dict[selected_file]
# ---------------------------------------------------------------------------------------------


st.divider()
# ---------------------------------------------------------------------------------------------
# Tabs
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Column Management",
        "Invalid Data Handling",
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
                options=DATA_TYPE_OPTIONS,
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
            key=f"{selected_df}'s_column_drop_list",
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

    column_fil_formulas = []

    col1, col2, col3, col4 = st.columns([0.3, 0.15, 0.15, 0.4])

    with col1:
        new_col_name = st.text_input(
            label="Column Name", placeholder="Name of the Column", key="new_col_name"
        )
    with col2:
        new_col_dtype = st.selectbox(
            label="Data Type", options=DATA_TYPE_OPTIONS, index=3, key="new_col_dtype"
        )
    with col3:
        new_col_mode = st.radio(
            label="Fill Type",
            options=["Same Value", "Formula"],
            horizontal=True,
            key="new_col_mode",
        )
    with col4:
        if new_col_mode == "Same Value":
            new_col_value = display_type_based_input(new_col_dtype, "first_use")
            st.session_state.new_col_value = new_col_value
        elif new_col_mode == "Formula":
            new_col_formula = st.selectbox(
                label="Formula",
                options=column_fil_formulas,
                index=0,
                key="new_col_formula",
            )

    if new_col_mode == "Formula":
        display_function_options()

    st.button(label="Create Column", on_click=helper_create_column)
    if selected_file:
        selected_df = st.session_state.df_dict[selected_file]

    st.divider()
    # ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------
with tab2:
    # Missing Data Operations
    st.header("Missing Data Operations")

    # ---------------------------------------------------------------------------------------------
    # Drop Rows
    st.subheader("Drop Rows with NaN")
    null_rows = selected_df.isnull().any(axis=1).sum()
    st.info(f"Rows Containing Null Values: **{null_rows}**")

    row_drop_list_by_column = st.pills(
        label="Drop Rows in Selected Columns",
        options=selected_df.columns,
        selection_mode="multi",
        key=f"row_drop_list_by_{selected_df}'s_column",
    )
    if len(row_drop_list_by_column) > 0:
        col_amount_to_drop = len(row_drop_list_by_column)
    else:
        col_amount_to_drop = "All"

    drop_row_button = st.button(
        label=f"Drop Null from {col_amount_to_drop} Column(s)",
        on_click=helper_drop_null_rows,
    )

    if selected_file:
        selected_df = st.session_state.df_dict[selected_file]

    st.divider()
    # ---------------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------------
    # Fill Null Values
    st.subheader("Fill NaN")
    col1, col2 = st.columns([0.6, 0.4])

    with col1:
        fill_null_list_by_column = st.pills(
            label="Select Columns to Fill",
            options=selected_df.columns,
            selection_mode="single",
            key=f"fill_null_by_{selected_df}'s_column",
        )
    with col2:
        select_fill_options = st.selectbox(
            label="Fill Method", options=FILL_OPTIONS, key="fill_method"
        )

    if select_fill_options == "Custom":
        col1, col2 = st.columns([0.3, 0.7])

        with col1:
            data_type = st.selectbox(label="Data Type", options=DATA_TYPE_OPTIONS)
        with col2:
            custom_value_fill = display_type_based_input(data_type, "second_use")
            st.session_state.custom_value_fill = custom_value_fill

    st.button(label="Fill Null Values", on_click=helper_fill_null_values)

    if selected_file:
        selected_df = st.session_state.df_dict[selected_file]

    st.divider()
    # ---------------------------------------------------------------------------------------------

    # Duplicate Rows Operations
    st.header("Duplicate Rows")
    # ---------------------------------------------------------------------------------------------
    # Remove Duplicate Rows
    st.subheader("Remove Duplicate Rows")
    duplicated_amount, duplicated_rows = info_duplicate_rows(selected_df)

    if duplicated_amount > 0:
        st.info("Only the Duplicated Row after the first one is shown")
        st.dataframe(duplicated_rows)
        st.button(
            f"Delete {duplicated_amount} Rows",
            on_click=helper_drop_duplicate_rows,
            use_container_width=True,
        )
    else:
        st.success("No Duplicate Rows")

    if selected_file:
        selected_df = st.session_state.df_dict[selected_file]
    # ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------
with tab3:
    st.header("Filter Dataset")
    # ---------------------------------------------------------------------------------------------
    # Filter by Value:
    st.subheader("Filter Method")
    filter_method = st.segmented_control(
        label="Select the Filter Method:",
        options=["Comparison", "Index Range"],
        key="filter_method",
    )

    if filter_method == "Comparison":
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            column_name = st.selectbox(
                "Select Column", selected_df.columns, key="filter_column_name"
            )
        with col2:
            comparison_operator = st.selectbox(
                "Select Operator",
                ["==", ">", ">=", "<", "<=", "Contains"],
                key="filter_comparison_operator",
            )
        with col3:
            filter_data_type = st.selectbox("Select DataType", DATA_TYPE_OPTIONS)
        with col4:
            filter_value = display_type_based_input(filter_data_type, "third_use")
            st.session_state.filter_value = filter_value

        st.button("Filter", on_click=info_filter_dataset)

    elif filter_method == "Index Range":
        col1, col2 = st.columns(2)
        with col1:
            index_from = st.number_input(
                label="Index From:",
                min_value=0,
                max_value=len(selected_df) - 1,
                step=1,
                key="index_from",
            )
        with col2:
            index_until = st.number_input(
                label="Index Until:",
                min_value=0,
                max_value=len(selected_df) - 1,
                step=1,
                key="index_until",
            )

        if st.button("Filter"):
            filtered_df = selected_df.iloc[index_from:index_until]
            st.session_state.filtered_df = filtered_df

    st.dataframe(st.session_state.get("filtered_df"))

    # ---------------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
