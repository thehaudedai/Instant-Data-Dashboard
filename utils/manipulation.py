import streamlit as st
import pandas as pd
import datetime


# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------


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


# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------


def helper_drop_columns():
    selected_file = st.session_state.get("selected_file")
    df_dict = st.session_state.get("df_dict")
    drop_list = st.session_state.get(f"{df_dict[selected_file]}'s_column_drop_list")

    if not selected_file or not df_dict or not drop_list:
        return

    df = df_dict[selected_file].copy()

    if len(drop_list) >= 1:
        df.drop(drop_list, axis=1, inplace=True)
        st.session_state.df_dict[selected_file] = df


# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------


def helper_create_column():
    selected_file = st.session_state.get("selected_file")
    df_dict = st.session_state.get("df_dict")

    name = st.session_state.get("new_col_name")
    dtype = st.session_state.get("new_col_dtype")
    mode = st.session_state.get("new_col_mode")

    if mode == "Same Value":
        value = st.session_state.get("new_col_value")
    else:
        formula = st.session_state.get("new_col_")

    if not selected_file or not df_dict or not name:
        return

    df = df_dict[selected_file].copy()

    if mode == "Same Value":
        df[name] = value
    elif mode == "Formula":
        # TODO: Implement How the formulas should be handled
        pass

    df[name] = df[name].astype(dtype)

    st.session_state.df_dict[selected_file] = df
    del st.session_state["new_col_name"]


# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------


# def helper_drop_duplicate_rows():
#     selected_file = st.session_state.get("selected_file")
#     df_dict = st.session_state.get("df_dict")

#     if not selected_file or not df_dict:
#         return

#     df = df_dict[selected_file].copy()

#     df = df.drop_duplicates(keep="first", ignore_index=True)
#     st.session_state.df_dict[selected_file] = df

# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------


def helper_drop_null_rows():
    selected_file = st.session_state.get("selected_file")
    df_dict = st.session_state.get("df_dict")

    if not selected_file or not df_dict:
        return

    df = df_dict[selected_file].copy()
    drop_list = st.session_state.get(
        f"row_drop_list_by_{df_dict[selected_file]}'s_column"
    )

    if len(drop_list) > 0:
        df = df.dropna(subset=drop_list).reset_index(drop=True)
    else:
        df = df.dropna().reset_index(drop=True)

    st.session_state.df_dict[selected_file] = df


# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------


def helper_fill_null_values():
    selected_file = st.session_state.get("selected_file")
    df_dict = st.session_state.get("df_dict")
    fill_method = st.session_state.get("fill_method")

    if not selected_file or not df_dict or not fill_method:
        return

    col = st.session_state.get(f"fill_null_by_{df_dict[selected_file]}'s_column")
    df = df_dict[selected_file].copy()

    try:
        if fill_method == "Custom":
            value = st.session_state.get("custom_value_fill")
            if not value:
                return
            else:
                df[col] = df[col].fillna(value)
        elif fill_method == "Mean":
            df[col] = df[col].fillna(df[col].mean())
        elif fill_method == "Median":
            df[col] = df[col].fillna(df[col].median())
        elif fill_method == "Mode":
            df[col] = df[col].fillna(df[col].mode()[0])
        elif fill_method == "Forward Fill":
            df[col] = df[col].fillna(method="ffill")
        elif fill_method == "Backward Fill":
            df[col] = df[col].fillna(method="bfill")
        else:
            return
    except:
        return

    st.session_state.df_dict[selected_file] = df


# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------
