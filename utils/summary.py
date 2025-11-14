import pandas as pd
import streamlit as st


def info_shape(df):
    row = df.shape[0]
    column = df.shape[1]

    return row, column


def info_dtypes(df, column):
    data_type = df[column].dtype
    return data_type


def info_nulls(df, column):
    null_amount = df[column].isnull().sum()
    return null_amount


def info_uniques(df, column):
    unique_amount = df[column].nunique()
    return unique_amount


def info_duplicate_rows(df: pd.DataFrame):
    duplicate_amount = df.duplicated().sum()
    duplicated_rows_df = df[df.duplicated()]
    return duplicate_amount, duplicated_rows_df


def info_sample_rows(df: pd.DataFrame, number, random=True, start="Head"):
    if random:
        return df.sample(n=number)
    else:
        if start == "Head":
            return df.head(number)
        elif start == "Tail":
            return df.tail(number)


def info_summary(df):
    summary_rows = []
    for column_name in df:
        summary_rows.append(
            {
                "Column Name": column_name,
                "Data Type": info_dtypes(df, column_name),
                "Distinct Values": info_uniques(df, column_name),
                "Missing Values": info_nulls(df, column_name),
            }
        )

    summary_df = pd.DataFrame(summary_rows)
    return summary_df


def info_filter_dataset():
    selected_file = st.session_state.get("selected_file")
    df_dict = st.session_state.get("df_dict")

    if not selected_file or not df_dict:
        return

    df = df_dict[selected_file].copy()

    method = st.session_state.get("filter_method")

    if method == "Comparison":
        column = st.session_state.get("filter_column_name")
        operator = st.session_state.get("filter_comparison_operator")
        value = st.session_state.get("filter_value")
    elif method == "Index Range":
        pass

    if method == "Comparison":
        try:
            match operator:
                case "==":
                    df = df[df[column] == value]
                case ">":
                    df = df[df[column] > value]
                case ">=":
                    df = df[df[column] >= value]
                case "<":
                    df = df[df[column] < value]
                case "<=":
                    df = df[df[column] <= value]
                case "!=":
                    df = df[df[column] != value]
                case "Contains":
                    df = df[df[column].str.contains(value, na=False)]
        except:
            pass

    st.session_state.filtered_df = df
