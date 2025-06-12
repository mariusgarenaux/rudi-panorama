import streamlit as st

st.set_page_config(page_title="RUDI Panorama - Summary", layout="wide", page_icon="🔭")

from utils.node_reader import (
    load_all_checked_node_readers,
    display_nodes_names_with_checkbox,
    initialize_node_list,
    load_one_node_reader,
    boost_node_info,
)
from rudi_node_read.rudi_node_reader import RudiNodeReader


def show_node_summary(node_url: str):
    load_one_node_reader(node_url)
    node_reader_boosted = st.session_state["all_node_readers"][node_url]
    node_reader = node_reader_boosted["node_reader"]
    with st.container(border=True):
        st.html(
            "<style>"
            "a, a:visited, a:hover, a:active {color: inherit;}"
            "</style>"
            f"<h2 style='color:{node_reader_boosted['color']}'><a href='{each_node_url}'>{each_node_url}</a></h3>"
        )

        st.markdown(
            f"""
        - Metadata count : {node_reader.metadata_count}
        
        - Keywords : {node_reader.keywords}

        """
        )


def add_node():
    if "added_node_url" not in st.session_state:
        st.warning("Could not add a node url.")
        return
    new_node_url = st.session_state.added_node_url
    if new_node_url in st.session_state["nodes_url_list"]:
        st.warning("The given URL is already on the list of nodes.")
        return
    try:
        nr_test = RudiNodeReader(new_node_url)
    except Exception as e:
        st.error(
            f"Could not add the given url : '{new_node_url}' because RudiNodeReader could not be loaded : '{e}'"
        )
        return
    else:
        st.session_state["nodes_url_list"][new_node_url] = boost_node_info(nr_test)
        load_all_checked_node_readers()


if __name__ == "__main__":
    st.markdown("# :rainbow[Catalogs Summary]")
    initialize_node_list()
    st.markdown("Here is a summary of checked nodes. See sidebar to check nodes.")
    # with st.container(border=True):
    #     st.markdown("#### Add a node")
    #     st.text_input("Node url :", key="added_node_url")
    #     st.button("Click here to add", on_click=add_node)

    display_nodes_names_with_checkbox()
    load_all_checked_node_readers()

    for each_node_url in st.session_state["nodes_url_list"]:
        if st.session_state[f"sidebar_checkbox {each_node_url}"]:
            show_node_summary(each_node_url)
