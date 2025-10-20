import streamlit as st
import pandas as pd


def helper_change_column_name():
    selected_file = st.session_state.get("selected_file")
    df_dict = st.session_state.get("df_dict")

    if not selected_file or not df_dict:
        return

    df = df_dict[selected_file].copy()  # Work on a copy
    renamed_dict = {}

    for column in df.columns:
        new_name = st.session_state.get(f"rename_{column}", column)
        if new_name and new_name != column:
            renamed_dict[column] = new_name

    if renamed_dict:
        df.rename(columns=renamed_dict, inplace=True)
        st.session_state.df_dict[selected_file] = df


def helper_drop_columns():
    selected_file = st.session_state.get("selected_file")
    df_dict = st.session_state.get("df_dict")
    drop_list = st.session_state.get("column_drop_list")

    if not selected_file or not df_dict or not drop_list:
        return

    df = df_dict[selected_file].copy()

    if len(drop_list) >= 1:
        df.drop(drop_list, axis=1, inplace=True)
        st.session_state.df_dict[selected_file] = df


def helper_drop_duplicate_rows():
    selected_file = st.session_state.get("selected_file")
    df_dict = st.session_state.get("df_dict")

    if not selected_file or not df_dict:
        return

    df = df_dict[selected_file].copy()

    df = df.drop_duplicates(keep="first", ignore_index=True)
    st.session_state.df_dict[selected_file] = df


def helper_filter_dataset():
    selected_file = st.session_state.get("selected_file")
    df_dict = st.session_state.get("df_dict")

    column_name = st.session_state.get("drop_row_column")
    operator = st.session_state.get("drop_row_operator")
    value = st.session_state.get("drop_row_value")
    data_type = st.session_state.get("drop_row_type")

    if (
        not selected_file
        or not df_dict
        or not column_name
        or not operator
        or value is None
        or not data_type
    ):
        st.warning("Please make sure all filter inputs are filled.")
        return

    df = df_dict[selected_file].copy()

    # Convert value to proper type
    try:
        match data_type:
            case "String":
                value = str(value)
            case "Integer":
                value = int(value)
            case "Float":
                value = float(value)
            case "Boolean":
                if isinstance(value, str) and value.lower() == "true":
                    value = True
                elif isinstance(value, str) and value.lower() == "false":
                    value = False
                else:
                    raise ValueError("Boolean value must be 'true' or 'false'")
    except ValueError as e:
        st.warning(f"Invalid value for type '{data_type}': {e}")
        return

    # Perform filtering with exception handling
    try:
        match operator:
            case "==":
                df_new = df[df[column_name] == value]
            case "!=":
                df_new = df[df[column_name] != value]
            case ">":
                df_new = df[df[column_name] > value]
            case ">=":
                df_new = df[df[column_name] >= value]
            case "<":
                df_new = df[df[column_name] < value]
            case "<=":
                df_new = df[df[column_name] <= value]
            case "Contains":
                if not isinstance(value, str):
                    st.warning("'Contains' operator only works with string values.")
                    return
                df_new = df[
                    df[column_name].astype(str).str.contains(str(value), na=False)
                ]
            case _:
                st.warning(f"Unknown operator: {operator}")
                return
    except Exception as e:
        st.warning(f"Error while filtering: {e}")
        return

    st.session_state.drop_row_df = df_new


def helper_drop_displayed_rows():
    selected_file = st.session_state.get("selected_file")
    df_dict = st.session_state.get("df_dict")
    df_to_delete = st.session_state.get("drop_row_df")

    if not selected_file or not df_dict or df_to_delete is None:
        return

    df = df_dict[selected_file].copy()

    df = df.drop(df_to_delete.index)
    st.session_state.df_dict[selected_file] = df
    st.session_state.drop_row_df = None
