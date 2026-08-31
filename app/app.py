import streamlit as st


st.set_page_config(
    page_title="Nashville Urban Operations Intelligence Platform",
    page_icon="🏙️",
    layout="wide"
)


st.title("Nashville Urban Operations Intelligence Platform")

st.write(
    "A data engineering and analytics platform for exploring "
    "urban operations data in Nashville."
)


st.subheader("Project Dashboard")

column1, column2, column3 = st.columns(3)

with column1:
    st.metric(
        label="Data Sources",
        value="0"
    )

with column2:
    st.metric(
        label="Records Processed",
        value="0"
    )

with column3:
    st.metric(
        label="Last Update",
        value="Not Available"
    )


st.divider()

st.subheader("About the Project")

st.write(
    """
    This platform will collect, clean, transform, store, and analyze
    Nashville urban operations data.

    The final system will use a data engineering pipeline and
    Streamlit for interactive analysis and visualization.
    """
)