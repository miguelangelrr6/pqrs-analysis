import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
from collections import Counter
import matplotlib.pyplot as plt
import re
import string 
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


st.set_page_config(
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

st.write("# VOCABULARIO PQRSD")

df_pqr = pd.read_csv("ps_PQRSD.csv", sep = ';',
                     header = 0,
                     names = ["No_Expediente", "Tipo_Documental", "No_Radicado", "Titulo_asunto","Archivado",
                              "Fecha_creacion","Dependencia","Origen","Usuario_creador","Expediente_asociado"],
                     parse_dates = ['Fecha_creacion'])


def pa():
	op = ('NUBE DE PALABRAS', 'DIFERENCIA DE VOCABULARIO')
	opt = list(range(len(op)))
	pnt = st.sidebar.selectbox('ANALISIS VISUAL DEL VOCABULARIO', opt, format_func = lambda x: op[x])
	return pnt
reductions_type = pa()

if reductions_type == 0:
    st.sidebar.success("SELECCIONAR EL INTERVALO DE FRECUENCIA DE PALABRAS A MOSTRAR EN LA NUBE DE PALABRAS")
    BAJA_FRECUENCIA = st.sidebar.number_input(label = 'BAJA FRECUENCIA', min_value = 0.0000,
                                              max_value = 100.0000,
                                              value = 0.4900)

    ALTA_FRECUENCIA = st.sidebar.number_input(label = 'ALTA FRECUENCIA', min_value = 0.0000,
                                              max_value = 100.0000 ,
                                              value = 100.0000)

                   
    nltk.download('stopwords')
    sw = stopwords.words('spanish')
    text = " ".join(i for i in df_pqr.Titulo_asunto)
    wc = WordCloud(stopwords = sw, collocations=False,).generate(text)
    d = dict((k, v) for k, v in wc.words_.items() if (ALTA_FRECUENCIA/100) > v >= (BAJA_FRECUENCIA/100))
    wc = WordCloud(width=1600, height=800).generate_from_frequencies(d)
    plt.figure(figsize=(20,10))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show()
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()
    
if reductions_type == 1:
    nltk.download('stopwords')
    sw = stopwords.words('spanish')
    
    def pa1():
        op1 = ('MESES', 'INTERVALOS DE TIEMPO')
        opt1 = list(range(len(op1)))
        pnt1 = st.sidebar.selectbox('DIFERENCIAS EN FUNCION A', opt1, format_func = lambda x: op1[x])
        return pnt1
    rt1 = pa1()
    
    if rt1 == 0:
        mes = ['Enero', 'Febrero', 'Marzo','Abril','Mayo','Junio',
                    'Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
        def pa10():
            op10 = ('Enero', 'Febrero', 'Marzo','Abril','Mayo','Junio',
                    'Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre')
            opt10 = list(range(len(op10)))
            m1 = st.sidebar.selectbox('MES 1', opt10, format_func = lambda x: op10[x])
            m2 = st.sidebar.selectbox('MES 2', opt10, format_func = lambda x: op10[x])
            return m1, m2
        k1, k2 = pa10()
        
        if k1 != k2:
            st.write('# DIFERENCIA ENTRE', mes[k1].upper() , 'y', mes[k2].upper())
            st.write('SE MOSTRARA LA DIFERENCIA ENTRE LOS 2 MESES POR MEDIO DEL ORDEN EN QUE SE SELECCIONEN.',
            '''SIENDO LA COMPARACION ENTRE FEBRERO Y MARZO, LAS PALABRAS NUEVAS QUE SE ESTAN USANDO EN FEBRERO, LAS QUE SE DEJARON DE
            UTILIZAR EN MARZO Y SI ESTAS PALABRAS SE ESTAN USANDO MAS O MENOS EN LOS PQRSD EMITIDOS EN ESTOS MESES.
            SIENDO VOCABULARIO ADQUIRIDO EL QUE AUMENTA SU FRECUENCIA O EL ENRIQUECIDO y VOCABULARIO ELIMINADO ES EL QUE DISMIUYE EN
            FRECUENCIA O SE VE SUSTRAIDO''')
            w1 = WordCloud(stopwords = sw, collocations=False,).generate(
                " ".join(i for i in df_pqr[df_pqr.Fecha_creacion.dt.month == k1+1].Titulo_asunto))
            w2 = WordCloud(stopwords = sw, collocations=False,).generate(
                " ".join(i for i in df_pqr[df_pqr.Fecha_creacion.dt.month == k2+1].Titulo_asunto))
            wc1 = dict((k, v) for k, v in w1.words_.items())
            wc2 = dict((k, v) for k, v in w2.words_.items())
            #dict frq positive change and new words
            d1 ={k: wc1.get(k, 0) - wc2.get(k, 0) for k in set(wc1) | set(wc2) if wc1.get(k, 0) - wc2.get(k, 0) > 0}
            #dict frq negative change and words erased
            d2 = {k: abs(wc1.get(k, 0) - wc2.get(k, 0)) for k in set(wc1) | set(wc2) if wc1.get(k, 0) - wc2.get(k, 0) < 0}
            
            def pa101():
                op101 = ('VOCABULARIO ADQUIRIDO EN ' + mes[k1].upper(),
                         'VOCABULARIO ELIMINADO EN ' + mes[k2].upper())
                opt101 = list(range(len(op101)))
                ld = st.sidebar.selectbox('MES 1', opt101, format_func = lambda x: op101[x])
                return ld
            k11 = pa101()
            
            if k11 == 0:
                wcp1 = WordCloud(width=1600, height=800).generate_from_frequencies(d1)
                plt.figure(figsize=(20,10))
                plt.imshow(wcp1, interpolation='bilinear')
                plt.axis("off")
                plt.tight_layout(pad=0)
                plt.show()
                st.set_option('deprecation.showPyplotGlobalUse', False)
                st.pyplot()
            else:
                wcp2 = WordCloud(width=1600, height=800).generate_from_frequencies(d1)
                plt.figure(figsize=(20,10))
                plt.imshow(wcp2, interpolation='bilinear')
                plt.axis("off")
                plt.tight_layout(pad=0)
                plt.show()
                st.set_option('deprecation.showPyplotGlobalUse', False)
                st.pyplot()
                
    else:
        date1 = st.sidebar.date_input("Selecciona la fecha inicial", value = dt.datetime(2019,1,1), key= "1", min_value = dt.datetime(2019,1,1), max_value = dt.datetime(2022,12,11))
        date2 = st.sidebar.date_input("Selecciona la fecha final", value = dt.datetime(2022,12,31), key= "2", min_value = dt.datetime(2019,1,1), max_value = dt.datetime(2022,12,31))
        cond1 = (df_pqr.Fecha_creacion > np.datetime64(date1)) & (df_pqr.Fecha_creacion < np.datetime64(date2))
        
        if (date1 < date2) & (len(df_pqr.loc[cond1]) > 0):
            st.write('DIFERENCIA ENTRE', date1 , 'y', date2)   
            
            w101 = WordCloud(stopwords = sw, collocations=False,).generate(
                " ".join(i for i in df_pqr.loc[cond1].Titulo_asunto))
            d101 = dict((k, v) for k, v in w101.words_.items())
            wcp101 = WordCloud(width=1600, height=800).generate_from_frequencies(d101)
            plt.figure(figsize=(20,10))
            plt.imshow(wcp101, interpolation='bilinear')
            plt.axis("off")
            plt.tight_layout(pad=0)
            plt.show()
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.pyplot()
            
        else:
            st.write('INTERVALO INCOMPATIBLE O CON CERO DATOS')
