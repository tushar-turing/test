import streamlit as st
from text_classification.main import render_intent_classification_page, render_ten_classification_page, \
    render_text_to_option

st.set_page_config(
    page_title="Turing | Amazon Benchmarks",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
        img[data-testid="stLogo"] {
            height: 3.5rem;
        }
    </style>
    """
    ,
    unsafe_allow_html=True,
)

# image_path = "./images/turing-logo-white.png" if st.context.theme.type == "dark" else "./images/turing-logo.png"

# st.logo(image_path, size="large")
st.sidebar.title("Amazon Benchmarks")

if st.sidebar.button("Reset State", use_container_width=True):
    st.session_state.clear()
    st.rerun()

# Navigation
page = st.sidebar.selectbox(
    "Choose a page:",
    ["Intent Classification", "TEN Classification", "Text2Options", "BFCL"]
)

if page == "Intent Classification":
    st.markdown('<h1 class="main-header">Intent Classification</h1>', unsafe_allow_html=True)
    render_intent_classification_page()

elif page == "TEN Classification":
    st.markdown('<h1 class="main-header">TEN Classification</h1>', unsafe_allow_html=True)
    render_ten_classification_page()

elif page == "Text2Options":
    st.markdown('<h1 class="main-header">Text2Options</h1>', unsafe_allow_html=True)
    render_text_to_option()

elif page == "BFCL":
    st.markdown('<h1 class="main-header">BFCL</h1>', unsafe_allow_html=True)
    st.write("This is the BFCL page")

# Footer
st.markdown("---")
st.markdown("""<div style='text-align: center; color: #666;'>
    <p> <a href="https://turing.com">Turing</a> | Amazon Benchmarks</p>
</div>""", unsafe_allow_html=True)
