import streamlit as st
import os

st.set_page_config(page_title="RUDI Panorama", layout="wide", page_icon="🔭")

from utils.node_reader import (
    load_all_checked_node_readers,
    initialize_node_list,
    load_one_node_reader,
    display_nodes_names_with_checkbox,
    initialize_nodes_colors,
)


def change_body_checkbox(node_url):
    st.session_state[f"sidebar_checkbox {node_url}"] = st.session_state[
        f"body {node_url}"
    ]


def display_all_metadatas():

    for each_node_url in st.session_state["nodes_url_list"]:
        # st.checkbox(
        #     label=f"### {each_node_url} ({each_node_reader.metadata_count})",
        #     key=f"body {each_node_url}",
        #     value=st.session_state[f"sidebar_checkbox {each_node_url}"],
        #     on_change=change_body_checkbox,
        #     kwargs={"node_url": each_node_url},
        # )
        if st.session_state[f"sidebar_checkbox {each_node_url}"]:
            display_metadata_catalog(each_node_url)


def display_metadata_catalog(each_node_url: str):
    load_one_node_reader(each_node_url)
    node_reader_boosted = st.session_state["all_node_readers"][each_node_url]
    node_reader = node_reader_boosted["node_reader"]

    st.html(
        "<style>"
        "a, a:visited, a:hover, a:active {color: inherit;}"
        "</style>"
        f"<h2 style='color:{node_reader_boosted['color']}'><a href='{each_node_url}'>{each_node_url}</a></h3>"
    )

    if node_reader.metadata_count == 0:
        st.write(f"No metadata for {node_reader.server_url}")
        return
    for each_metadata in node_reader.metadata_list:
        nice_medias = get_nice_medias(each_metadata)
        metadata_url = os.path.join(
            node_reader.server_url, "catalog/v1/resources", each_metadata["global_id"]
        )
        with st.container(border=True):
            st.html(
                "<style>"
                "a, a:visited, a:hover, a:active {color: inherit;}"
                "</style>"
                f"<h3 style='color:{node_reader_boosted['color']}'><a href='{metadata_url}'>{each_metadata['resource_title']}</a></h3>"
            )
            # st.markdown(f"#### [:green[]]({metadata_url})")
            st.markdown(
                f":orange[_**Summary**_] : {each_metadata['summary'][0]['text']}"
            )
            st.markdown(f":orange[_**Medias**_] : \n {nice_medias}")


# - Medias : {nice_medias}


@st.cache_data
def get_nice_medias(rudi_metadata: dict):
    res = ""
    for each_media in rudi_metadata["available_formats"]:
        res += f"- {each_media['media_name']} : {each_media['connector']['url']} \n"
    return res


def sort_by_metadata_count():
    all_nr = st.session_state.all_node_readers
    st.session_state.all_node_readers = {
        key: value
        for key, value in sorted(
            all_nr.items(), key=lambda item: item[1].metadata_count, reverse=True
        )
    }
    st.session_state.nodes_url_list = list(st.session_state.all_node_readers.keys())


def sort_by_alphabetical_order():
    all_nr = st.session_state.all_node_readers
    st.session_state.all_node_readers = {
        key: value
        for key, value in sorted(all_nr.items(), key=lambda item: item[1].server_url)
    }
    st.session_state.nodes_url_list = list(st.session_state.all_node_readers.keys())


def sort_metadata():
    if st.session_state.sort_toggle:
        sort_by_metadata_count()
    else:
        sort_by_alphabetical_order()


import base64


def get_base64(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = (
        """
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    """
        % bin_str
    )
    st.markdown(page_bg_img, unsafe_allow_html=True)


if __name__ == "__main__":
    initialize_node_list()
    initialize_nodes_colors()
    display_nodes_names_with_checkbox()
    load_all_checked_node_readers()
    st.markdown("# :rainbow[RUDI Panorama 🔭]")

    st.markdown(
        "This website allows you to have a panorama of metadatas availables on a list of RUDI nodes."
    )

    st.markdown("Select the one you want to explore in the sidebar")
    # st.toggle(
    #     label="Sort by metadata count",
    #     key="sort_toggle",
    #     value=False,
    #     on_change=sort_metadata,
    # )

    display_all_metadatas()
