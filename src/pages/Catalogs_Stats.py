import streamlit as st

st.set_page_config(layout="wide", page_icon="🔭")

from utils.node_reader import display_nodes_names_with_checkbox


if __name__ == "__main__":

    st.markdown("# Page 3 🎉")
    st.sidebar.markdown("# Page 3 🎉")
    display_nodes_names_with_checkbox(sidebar=True)
