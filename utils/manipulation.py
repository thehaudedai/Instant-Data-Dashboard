import streamlit as st
import pandas as pd


def helper_change_column_name():
    selected_file = st.session_state.get("selected_file")
    df_dict = st.session_state.get("df_dict")

    if not selected_file or not df_dict:
        return

    current_df = df_dict[selected_file].copy()  # Work on a copy
    renamed_dict = {}

    for column in current_df.columns:
        new_name = st.session_state.get(f"rename_{column}", column)
        if new_name and new_name != column:
            renamed_dict[column] = new_name

    if renamed_dict:
        current_df.rename(columns=renamed_dict, inplace=True)
        st.session_state.df_dict[selected_file] = current_df
