import streamlit as st

st.set_page_config(layout="wide", page_icon="🔭")

from utils.node_reader import (
    initialize_node_list,
    display_nodes_names_with_checkbox,
    get_fancy_node_list,
)


if __name__ == "__main__":
    st.markdown("# RUDI Panorama 🔭")

    initialize_node_list()

    st.markdown(
        "This website allows you to have a panorama of metadatas availables on a list of RUDI nodes."
    )

    st.markdown(
        "Here is the list of available nodes (same in the sidebar), select the one you want to explore :"
    )
    display_nodes_names_with_checkbox(sidebar=True)
    display_nodes_names_with_checkbox()
