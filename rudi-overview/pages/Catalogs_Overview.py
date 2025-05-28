from utils.node_reader import initialize_node_readers
import streamlit as st
from rudi_node_read.rudi_node_reader import RudiNodeReader


def display_nodes_names_in_sidebar():
    for each_node_url in st.session_state.all_node_readers:
        st.sidebar.checkbox(
            label=each_node_url, value=False, key=f"sidebar {each_node_url}"
        )


def change_body_checkbox(node_url):
    st.session_state[f"sidebar {node_url}"] = st.session_state[f"body {node_url}"]


def display_all_metadatas():
    for each_node_reader in st.session_state.all_node_readers.values():
        node_url = each_node_reader.server_url
        if f"sidebar {node_url}" not in st.session_state:
            return

        st.divider()
        st.checkbox(
            label=f"### {node_url} ({each_node_reader.metadata_count})",
            key=f"body {node_url}",
            value=st.session_state[f"sidebar {node_url}"],
            on_change=change_body_checkbox,
            kwargs={"node_url": node_url},
        )
        st.divider()
        if st.session_state[f"sidebar {node_url}"]:
            display_metadata_catalog(each_node_reader)


def display_metadata_catalog(node_reader: RudiNodeReader):
    if node_reader.metadata_count == 0:
        st.write(f"No metadata for {node_reader.server_url}")
        return
    for each_metadata in node_reader.metadata_list:
        nice_medias = get_nice_medias(each_metadata)
        with st.container(border=True):
            st.markdown(f"#### :green[{each_metadata['resource_title']}]")
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


def sort_by_alphabetical_order():
    all_nr = st.session_state.all_node_readers
    st.session_state.all_node_readers = {
        key: value
        for key, value in sorted(all_nr.items(), key=lambda item: item[1].server_url)
    }


def sort_metadata():
    if st.session_state.sort_toggle:
        sort_by_metadata_count()
    else:
        sort_by_alphabetical_order()


if __name__ == "__main__":
    initialize_node_readers()
    display_nodes_names_in_sidebar()
    st.markdown("# Catalogs overview")
    st.toggle(
        label="Sort by metadata count",
        key="sort_toggle",
        value=False,
        on_change=sort_metadata,
    )

    display_all_metadatas()
