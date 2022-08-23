import streamlit as st
from bokeh.models.widgets import Div
from PIL import Image

st.set_page_config(layout='wide',
    page_title="Pasaportes",
    page_icon="🛂",
)

image = Image.open('images/logo-gobernacion.png')
st.image(image, caption='Gobernación de Boyacá')

hide_menu_style = """
        <style>
        div.css-1r6slb0.e1tzin5v2{
            background-color: #DCDCDC;
            padding: 3% 3% 3% 3%;
            border-radius: 5px;
            }
        div.css-12w0qpk.e1tzin5v2{
            background-color: #DCDCDC;
            padding: 3% 3% 3% 3%;
            border-radius: 5px;
            }
        .css-k0sv6k.e8zbici2 {
            background-color: #349D60;
            color: white;
            }
        .css-1siy2j7.e1fqkh3o3 {
            background-color: rgba(52, 157, 96, 0.2);
            }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

st.write("# Bienvenido a control interno PQRSD 🛂")

if st.button('Volver al EDA'):
    js = "window.open('https://miguelangelrr6-sandbox-boyaca-app-hyj1lb.streamlitapp.com/')"  # New tab or window
    js = "window.location.href = 'https://miguelangelrr6-sandbox-boyaca-app-hyj1lb.streamlitapp.com/'"  # Current tab
    html = '<img src onerror="{}">'.format(js)
    div = Div(text=html)
    st.bokeh_chart(div)
