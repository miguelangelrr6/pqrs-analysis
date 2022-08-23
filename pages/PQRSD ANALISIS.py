from mimetypes import init
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import re
import string 
from collections import Counter
from PIL import Image
from datetime import date


st.set_page_config(layout='wide',
    page_title="Pasaportes",
    page_icon="🛂",
)

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


image = Image.open('images/logo-gobernacion.png')
st.sidebar.image(image, caption='Gobernación de Boyacá')


nltk.download('punkt')
nltk.download('stopwords')
sw = stopwords.words('spanish')

STOP_WORDS = stopwords.words()


st.write("# FILTROS PQRSD")

@st.cache
def get_PQRSD_data():
    df_pqr = pd.read_csv("ps_PQRSD.csv", sep = ';',
                     header = 0,
                     names = ["No_Expediente", "Tipo_Documental", "No_Radicado", "Titulo_asunto","Archivado",
                              "Fecha_creacion","Dependencia","Origen","Usuario_creador","Expediente_asociado"],
                     parse_dates = ['Fecha_creacion'])
    return df_pqr

df_pqr = get_PQRSD_data()

def cleaning(text):
    """
    Convert to lowercase.
    Rremove URL links, special characters and punctuation.
    Tokenize and remove stop words.
    """
    text = text.lower()
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('[’“”…]', '', text)

    # removing the stop-words
    text_tokens = word_tokenize(text)
    tokens_without_sw = [
        word for word in text_tokens if not word in STOP_WORDS]
    filtered_sentence = (" ").join(tokens_without_sw)
    text = filtered_sentence

    return text

dt = df_pqr.Titulo_asunto.apply(cleaning)

word_count = Counter(" ".join(dt).split()).most_common(10)
word_frequency = pd.DataFrame(word_count, columns = ['Word', 'Frequency'])


option = st.selectbox(
     'Selecciona una de las 10 palabras más comunes',
     word_frequency.Word)

st.write('Seleccionaste:', option)
data = df_pqr.loc[df_pqr.Titulo_asunto.str.lower().str.contains(option)]

st.dataframe(data)



#FILTER BY DATES
st.header("Nube de palabras por rango de fecha")

col1, col2= st.columns(2)

with col1:
    
    init_date = st.date_input(
        "Selecciona fecha inicio",
        date.today())
    st.write('Fecha inicio:', init_date)
with col2:
    end_date = st.date_input(
        "Selecciona fecha fin",
        date.today())
    st.write('Fecha fin:', end_date)

if (init_date <= end_date) and (init_date <= date.today() and end_date <= date.today()) and (len(df_pqr[(df_pqr.Fecha_creacion.dt.date >= init_date) & (df_pqr.Fecha_creacion.dt.date <= end_date)].Titulo_asunto) > 0):
                      
    df_pqr_date = df_pqr[(df_pqr.Fecha_creacion.dt.date >= init_date) & (df_pqr.Fecha_creacion.dt.date <= end_date)]

    text = " ".join(i for i in df_pqr_date.Titulo_asunto)

    wc = WordCloud(stopwords = sw, collocations=False,width=1600, height=500).generate(text)

    plt.figure(figsize=(10,5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show()
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()
elif init_date > date.today() or end_date > date.today():
    st.error("Seleccionaste una fecha posterior a la actual "+date.today().strftime("%Y/%m/%d"))
elif (init_date > end_date):
    st.error("Selecciona un rango de fechas correcto. Fecha inicio debe ser menor a fecha fin")
else:
    st.warning("No existen palabras en ese rango de fechas. Considera un rango anterior")

