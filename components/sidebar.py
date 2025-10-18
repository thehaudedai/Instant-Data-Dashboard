import streamlit as st


def render_sidebar():
    st.sidebar.title("Options")

    # Download button
    if "df_dict" in st.session_state and st.session_state.get("df_dict"):
        selected_file = st.sidebar.selectbox(
            "Choose file to download", list(st.session_state["df_dict"].keys())
        )
        df = st.session_state["df_dict"][selected_file]

        csv = df.to_csv(index=False).encode("utf-8")
        st.sidebar.download_button(
            label="Download CSV", data=csv, file_name=selected_file, mime="text/csv"
        )

    # Clear button
    if st.sidebar.button("Clear All Uploaded Files"):
        st.session_state.file_dict = {}
        st.session_state.df_dict = {}
        st.rerun()
