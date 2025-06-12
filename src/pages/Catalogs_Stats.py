import streamlit as st
from utils.node_reader import (
    load_all_checked_node_readers,
    initialize_node_list,
    load_one_node_reader,
)
from utils.tools import get_color_from_str
import pandas as pd

st.set_page_config(
    page_title="RUDI Panorama - Statistics", layout="wide", page_icon="🔭"
)

from utils.node_reader import display_nodes_names_with_checkbox


def display_node_readers_hist():
    keys, values, colors = [], [], []

    for each_node_url in st.session_state["nodes_url_list"]:
        if st.session_state[f"sidebar_checkbox {each_node_url}"]:
            load_one_node_reader(each_node_url)
            node_reader_boosted = st.session_state["all_node_readers"][each_node_url]
            node_reader = node_reader_boosted["node_reader"]
            keys.append(each_node_url)
            values.append(node_reader.metadata_count)
            colors.append(node_reader_boosted["color"])
    data = pd.DataFrame(data=values, index=pd.Index(keys), columns=pd.Index(["count"]))
    st.write(data)
    if len(keys) == 1:
        return
    st.bar_chart(data=data.transpose(), color=colors, horizontal=True)
    return


if __name__ == "__main__":

    st.markdown("# :rainbow[Catalogs Statistics]")
    st.markdown("Statistics about catalogs")
    initialize_node_list()
    display_nodes_names_with_checkbox()
    load_all_checked_node_readers()
    display_node_readers_hist()
