import streamlit as st

from rudi_node_read.rudi_node_reader import RudiNodeReader
import yaml
from utils.tools import CONFIG, get_color_from_str


def initialize_node_list():
    """
    Initialize the list of nodes urls from the config file, if not set in streamlit session state.
    """
    if "nodes_url_list" not in st.session_state:
        st.session_state["nodes_url_list"] = list(
            set(CONFIG["nodes_url_list"])
        )  # load from config and remove duplicates
    if len(st.session_state["nodes_url_list"]) > 50:
        st.warning(
            f"Be careful, you have more than 50 nodes registered and might be exceeding request quotas."
        )


def initialize_nodes_colors():
    st.session_state["nodes_colors"] = {
        each_node_url: get_color_from_str(each_node_url)
        for each_node_url in st.session_state["nodes_url_list"]
    }


def load_one_node_reader(node_url):
    """
    Safely loads a rudi-node-reader with error catching. Node reader is cached in streamlit session state.
    :param node_url: the url of the metadata catalog of the node (caution : no / at the end)
    """
    if node_url in st.session_state["all_node_readers"]:
        return
    try:
        nr = RudiNodeReader(server_url=node_url)
    except Exception as e:
        st.warning(f"Could not connect to node '{node_url}' : '{e}'")
    else:
        st.session_state.all_node_readers[node_url] = boost_node_info(nr)


def boost_node_info(nr: RudiNodeReader) -> dict:
    short_name = nr.server_url[8:].split(".")[0]
    return {
        "node_reader": nr,
        "short_name": short_name,
        "color": get_color_from_str(short_name),
    }


def load_all_checked_node_readers():
    """
    Loads the rudi-node-readers of the checked nodes url. They are only loaded once and cached in streamlit
    session state.
    """
    if "all_node_readers" not in st.session_state:
        st.session_state["all_node_readers"] = {}

    for each_node_url in st.session_state.nodes_url_list:
        if each_node_url in st.session_state.all_node_readers:
            continue
        if not st.session_state[
            f"sidebar_checkbox {each_node_url}"
        ]:  # do not load uncheck node
            continue
        load_one_node_reader(each_node_url)


def get_fancy_node_list():
    res = ""
    initialize_node_list()
    for each_node_url in st.session_state["nodes_url_list"]:
        res += f"- {each_node_url} \n"
    return res


def select_all_nodes():
    for each_node_url in st.session_state.nodes_url_list:
        st.session_state[f"sidebar_checkbox {each_node_url}"] = st.session_state[
            "sidebar toggle_select_all_nodes"
        ]
    return


def select_all_nodes_from_sidebar(key):
    keep_key(key)
    select_all_nodes()


def display_toggle_select_all():
    st.sidebar.toggle(
        key="_sidebar toggle_select_all_nodes",
        label="Select all",
        value=(
            st.session_state["sidebar toggle_select_all_nodes"]
            if "sidebar toggle_select_all_nodes" in st.session_state
            else False
        ),
        on_change=select_all_nodes_from_sidebar,
        kwargs={"key": "sidebar toggle_select_all_nodes"},
    )


def keep_key(key: str):
    st.session_state[key] = st.session_state[f"_{key}"]


def display_nodes_names_with_checkbox():
    display_toggle_select_all()
    for each_node_url in st.session_state.nodes_url_list:
        st.sidebar.checkbox(
            label=each_node_url,
            value=(
                st.session_state[f"sidebar_checkbox {each_node_url}"]
                if f"sidebar_checkbox {each_node_url}" in st.session_state
                else False
            ),
            key=f"_sidebar_checkbox {each_node_url}",
            on_change=keep_key,
            kwargs={"key": f"sidebar_checkbox {each_node_url}"},
        )
        keep_key(f"sidebar_checkbox {each_node_url}")
