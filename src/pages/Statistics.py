import streamlit as st

st.set_page_config(page_title="Statistics", layout="wide", page_icon="🔭")

from utils.node_reader import display_nodes_names_with_checkbox


if __name__ == "__main__":

    st.markdown("# Catalogs Statistics")
    st.markdown("Statistics about catalogs")
    display_nodes_names_with_checkbox(sidebar=True)
