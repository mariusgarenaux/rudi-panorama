import streamlit as st

st.set_page_config(page_title="RUDI Panorama - Graph", layout="wide", page_icon="🔭")

from sklearn.decomposition import PCA
import plotly.graph_objs as go
from utils.node_reader import (
    initialize_node_list,
    display_nodes_names_with_checkbox,
    load_all_checked_node_readers,
    load_one_node_reader,
)
from sentence_transformers import SentenceTransformer
import plotly.graph_objs as go


@st.cache_resource
def load_model(
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2", device: "str" = "cpu"
):
    """
    Loads either a word llama model or any model from sentence-transformer

    ### Parameters
        - model_name: name of any model (e.g. sentence-transformers/all-MiniLM-L6-v2) that
            can be loaded by sentence-transformer (https://www.sbert.net/)
        - device: string for torch.device where model is loaded (e.g. "mps", "cpu", ...).
            Default to "cpu".
    """
    if "btn load_model" in st.session_state and st.session_state["btn load_model"]:
        return SentenceTransformer(model_name, device=device)
    return


def display_keywords_embeddings(model_name: str, display_text: bool = False):
    """
    Display 2D embeddings of each keyword of each rudi node. Dimension of embeddings
    is reduced to 2 with PCA (Principal Component Analysis).

    ### Parameters
        - model_name: name of any model (e.g. sentence-transformers/all-MiniLM-L6-v2) that
            can be loaded by sentence-transformer (https://www.sbert.net/)
        - display_text: whether to display each keyword on the side of each point in the graph.
            Default to False

    ### Returns
        - None, just displays the graph
    """

    embedding_model = load_model(model_name)
    if embedding_model is None:
        return
    # st.write(embedding_model)
    embeddings = embedding_model.encode(text, convert_to_tensor=False)
    # st.write(embeddings)
    pca = PCA(n_components=2)
    embeddings_2d = pca.fit_transform(embeddings)

    trace_nodes = go.Scatter(
        x=embeddings_2d[:, 0],
        y=embeddings_2d[:, 1],
        mode="markers" if not display_text else "text+markers",
        text=text,
        textposition="top center",
        marker=dict(
            size=10,
            color=colors,
            # colorscale="Viridis",
            opacity=0.8,
        ),
    )

    layout = go.Layout(
        title=None,
        xaxis=dict(title=None, showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(title=None, showgrid=False, zeroline=False, showticklabels=False),
        margin=dict(l=0, r=0, b=0, t=0),
        showlegend=False,
    )

    fig = go.Figure(data=trace_nodes, layout=layout)

    st.plotly_chart(fig)


def get_and_format_nodes_keywords() -> tuple[list[str], list[str]]:
    """
    Access all keywords from selected rudi-nodes; and format them in a list. Creates a list
    of the same size with color of each node.

    ### Returns
        - a tuple (text, colors) where text is the list of keywords, and colors the
            list of hex colors of same length.
    """
    text = []
    colors = []
    for each_node_url in st.session_state["nodes_url_list"]:
        if st.session_state[f"sidebar_checkbox {each_node_url}"]:
            load_one_node_reader(each_node_url)
            node_reader_boosted = st.session_state["all_node_readers"][each_node_url]
            node_reader = node_reader_boosted["node_reader"]
            text += node_reader.keywords
            colors += len(node_reader.keywords) * [node_reader_boosted["color"]]
    # st.write(colors)
    # colors = [f"rgb{color}" for color in colors]
    return text, colors


def accept_loading_model():
    """
    Callback function called when load_model button is clicked.
    """
    st.session_state["accept_loading_model"] = True


def display_header():
    """
    Display the header of the page : title, text input and button. Loads checked node readers.
    """
    st.markdown("# :rainbow[Catalogs Graph]")
    st.markdown("Graphs about keywords in catalog")
    initialize_node_list()
    display_nodes_names_with_checkbox()
    load_all_checked_node_readers()
    st.markdown(
        "Enter one model from sentence-transformer (https://huggingface.co/sentence-transformers)"
    )
    st.markdown(
        """Example :\n - sentence-transformers/all-MiniLM-L6-v2 \n - sentence-transformers/static-similarity-mrl-multilingual-v1"""
    )
    st.toggle(label="Display keywords on graph", key="display_text")
    col1, col2 = st.columns([0.7, 0.3])
    with col1:
        st.text_input(
            label="model name",
            value="sentence-transformers/static-similarity-mrl-multilingual-v1",
        )
    with col2:
        st.button(
            label="Load model (⚠️ heavy)",
            key="btn load_model",
            on_click=accept_loading_model,
        )


if __name__ == "__main__":
    display_header()
    display_text = (
        st.session_state["display_text"]
        if "display_text" in st.session_state
        else False
    )
    model_name = (
        st.session_state["model_name"]
        if "model_name" in st.session_state
        else "sentence-transformers/static-similarity-mrl-multilingual-v1"
    )

    if (
        "accept_loading_model" in st.session_state
        and st.session_state["accept_loading_model"]
    ):
        text, colors = get_and_format_nodes_keywords()
        display_keywords_embeddings(model_name, display_text)
