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

    # selected_indices = []
    df_new["Select"] = False

    st.session_state.filtered_df = df_new
    # st.session_state.selected_index_df = selected_indices


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


def helper_apply_dtype_and_rename():
    selected_file = st.session_state.get("selected_file")
    df_dict = st.session_state.get("df_dict")
    editor_state = st.session_state.get("dtype_editor")

    if not selected_file or not df_dict or not editor_state:
        return

    df = df_dict[selected_file].copy()
    edited_rows = editor_state.get("edited_rows", {})

    for i, changes in edited_rows.items():
        old_col = df.columns[int(i)]
        new_col = changes.get("Column Name", old_col)
        new_dtype = changes.get("DataType")

        # Rename column if changed
        if new_col != old_col:
            df.rename(columns={old_col: new_col}, inplace=True)

        # Change dtype if changed
        if new_dtype and new_dtype != str(df[new_col].dtype):
            try:
                df[new_col] = df[new_col].astype(new_dtype)
            except Exception as e:
                st.warning(f"Could not convert {new_col} to {new_dtype}: {e}")

    st.session_state.df_dict[selected_file] = df
