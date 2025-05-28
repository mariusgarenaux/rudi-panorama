import streamlit as st

from rudi_node_read.rudi_node_reader import RudiNodeReader
import yaml
from utils.tools import CONFIG


def initialize_node_readers():
    if "node_url_list" not in st.session_state:
        st.session_state["nodes_url_list"] = CONFIG["nodes_url_list"]

    if "all_node_readers" not in st.session_state:
        st.session_state.all_node_readers = [
            RudiNodeReader(server_url=node_url)
            for node_url in st.session_state.nodes_url_list
        ]
