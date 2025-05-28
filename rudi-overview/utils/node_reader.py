import streamlit as st

from rudi_node_read.rudi_node_reader import RudiNodeReader
import yaml
from utils.tools import CONFIG


def initialize_node_readers():
    if "node_url_list" not in st.session_state:
        st.session_state["nodes_url_list"] = CONFIG["nodes_url_list"]

    if "all_node_readers" not in st.session_state:
        st.session_state["all_node_readers"] = {}

    if len(st.session_state["nodes_url_list"]) > 50:
        st.warning(
            f"Be careful, you have more than 50 nodes registered and might be exceeding request quotas."
        )
    for each_node_url in st.session_state.nodes_url_list:
        if each_node_url in st.session_state.all_node_readers:
            continue
        try:
            nr = RudiNodeReader(server_url=each_node_url)
        except Exception as e:
            st.warning(f"Could not connect to node '{each_node_url}' : '{e}'")
        else:
            st.session_state.all_node_readers[each_node_url] = nr
