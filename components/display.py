import streamlit as st
import pandas as pd
import datetime


# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------


def display_type_based_input(type):
    type = str(type)
    input_value = None
    first_input = None
    second_input = None

    if type in ["int64", "Int64"]:
        input_value = st.number_input(label="Value", placeholder="1024", step=1)

    elif type in ["float64", "Float64"]:
        input_value = st.number_input(
            label="Value", placeholder="223.28", step=0.001, format="%.6f"
        )

    elif type == "complex128":
        first_input = st.number_input("Real part", step=0.1)
        second_input = st.number_input("Imag part", step=0.01)
        input_value = complex(first_input, second_input)

    elif type == "boolean":
        input_value = st.toggle(label="True/False", value=False)

    elif type in ["string", "category", "object"]:
        input_value = st.text_input(label="Value", placeholder="Enter text")

    elif type == "datetime64[ns]" or type == "datetime64[ns, UTC]":
        first_input = st.date_input(label="Date Value", value=datetime.date.today())
        second_input = st.time_input(label="Time Value")
        combined = datetime.datetime.combine(first_input, second_input)
        if "UTC" in type:
            input_value = pd.Timestamp(combined, tz="UTC")
        else:
            input_value = pd.Timestamp(combined)

    elif type == "timedelta64[ns]":
        # Input number of days as a float, convert to timedelta
        days = st.number_input(
            label="Days (float)", step=0.25, placeholder="e.g. 2.5 for 2 days 12 hours"
        )
        input_value = pd.to_timedelta(days, unit="D")

    elif type == "period[M]":
        # Period by month
        date_value = st.date_input(label="Month period", value=datetime.date.today())
        input_value = pd.Period(date_value, freq="M")

    elif type == "period[Q]":
        # Period by quarter
        date_value = st.date_input(label="Quarter period", value=datetime.date.today())
        input_value = pd.Period(date_value, freq="Q")

    else:
        st.warning(f"Unsupported dtype: {type}")
        input_value = None

    return input_value


# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------


def display_function_options():
    pass


# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------
