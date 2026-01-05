# FOOTER
import base64
import streamlit as st





def get_base64_image(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def render_footer():
    github_base64 = get_base64_image("pages/images/GitHub_Lockup_Light.png")
    linkedin_base64 = get_base64_image("pages/images/LI-Logo.png")
    
    footer_html = f"""
    <div style="
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        text-align: center;
        padding: 5px 0;
        background-color: #111;
        z-index: 1000;
    ">
        <small style='color: white; font-size:12px;'>
            Made by Daniel Canlas | School of Statistics - University of the Philippines Diliman
        </small><br>
        <div style="display:flex; justify-content:center; align-items:center; gap:5px;">
            <a href='https://www.linkedin.com/in/danielkarlocanlas' target='_blank'>
                <img src='data:image/png;base64,{linkedin_base64}' width='50'>
            </a>
            <a href='https://github.com/dafencer' target='_blank'>
                <img src='data:image/png;base64,{github_base64}' width='50'>
            </a>
        </div>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)

