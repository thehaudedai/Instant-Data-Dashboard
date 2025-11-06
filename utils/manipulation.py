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
    drop_list = st.session_state.get("column_drop_list")

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


def helper_display_function_options():
    pass


# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------


def helper_display_type_based_input(type, key_name):
    type = str(type)  # normalize
    input_value = None

    if type in ["int64", "Int64"]:
        input_value = st.number_input(
            label="Value", placeholder="1024", step=1, key=key_name
        )

    elif type in ["float64", "Float64"]:
        input_value = st.number_input(
            label="Value", placeholder="223.28", step=0.001, format="%.6f", key=key_name
        )

    elif type == "complex128":
        real = st.number_input("Real part", step=0.1, key=f"{key_name}_real")
        imag = st.number_input("Imag part", step=0.1, key=f"{key_name}_imag")
        input_value = complex(real, imag)

    elif type == "boolean":
        input_value = st.toggle(label="True/False", value=False, key=key_name)

    elif type in ["string", "category", "object"]:
        input_value = st.text_input(
            label="Value", placeholder="Enter text", key=key_name
        )

    elif type == "datetime64[ns]" or type == "datetime64[ns, UTC]":
        date_value = st.date_input(label="Value", value="today", key=key_name)
        if type.endswith("UTC"):
            input_value = pd.Timestamp(date_value, tz="UTC")
        else:
            input_value = pd.Timestamp(date_value)

    elif type == "timedelta64[ns]":
        # Input number of days as a float, convert to timedelta
        days = st.number_input(
            label="Days (float)",
            step=0.25,
            placeholder="e.g. 2.5 for 2 days 12 hours",
            key=key_name,
        )
        input_value = pd.to_timedelta(days, unit="D")

    elif type == "period[M]":
        # Period by month
        date_value = st.date_input(label="Month period", value="today", key=key_name)
        input_value = pd.Period(date_value, freq="M")

    elif type == "period[Q]":
        # Period by quarter
        date_value = st.date_input(label="Quarter period", value="today", key=key_name)
        input_value = pd.Period(date_value, freq="Q")

    else:
        st.warning(f"Unsupported dtype: {type}")
        input_value = None

    return input_value


# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------
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
