import streamlit as st
import pandas as pd


def helper_change_column_name(df: pd.DataFrame, column, new_name):
    df.rename(columns={column: new_name}, inplace=True)
