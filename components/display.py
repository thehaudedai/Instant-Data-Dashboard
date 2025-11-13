import streamlit as st
import pandas as pd
import datetime


# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------


def display_type_based_input(type, key):
    type = str(type)
    input_value = None
    first_input = None
    second_input = None

    if type in ["int64", "Int64"]:
        input_value = st.number_input(
            label="Value", placeholder="1024", step=1, key=f"{type}_{key}"
        )

    elif type in ["float64", "Float64"]:
        input_value = st.number_input(
            label="Value",
            placeholder="223.28",
            step=0.001,
            format="%.6f",
            key=f"{type}_{key}",
        )

    elif type == "complex128":
        real = st.number_input("Real part", step=0.1, key=f"{type}_real_{key}")
        imag = st.number_input(
            "Imag part", step=0.01, format="%.4f", key=f"{type}_imag_{key}"
        )
        input_value = complex(real, imag)

    elif type == "boolean":
        input_value = st.toggle(label="True/False", value=False, key=f"{type}_{key}")

    elif type in ["string", "category", "object"]:
        input_value = st.text_input(
            label="Value", placeholder="Enter text", key=f"{type}_{key}"
        )

    elif type == "datetime64[ns]" or type == "datetime64[ns, UTC]":
        date_val = st.date_input(
            label="Date Value", value=datetime.date.today(), key=f"{type}_date_{key}"
        )
        time_val = st.time_input(label="Time Value", key=f"{type}_time_{key}")
        combined = datetime.datetime.combine(date_val, time_val)
        if "UTC" in type:
            input_value = pd.Timestamp(combined, tz="UTC")
        else:
            input_value = pd.Timestamp(combined)

    elif type == "timedelta64[ns]":
        days = st.number_input(
            label="Days (float)",
            step=0.25,
            placeholder="e.g. 2.5 for 2 days 12 hours",
            key=f"{type}_days_{key}",
        )
        input_value = pd.to_timedelta(days, unit="D")

    elif type == "period[M]":
        date_value = st.date_input(
            label="Month period", value=datetime.date.today(), key=f"{type}_date_{key}"
        )
        input_value = pd.Period(date_value, freq="M")

    elif type == "period[Q]":
        date_value = st.date_input(
            label="Quarter period",
            value=datetime.date.today(),
            key=f"{type}_date_{key}",
        )
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
