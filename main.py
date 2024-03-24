import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from postgresql_con import *

load_dotenv()

PASSWORD = os.getenv('PASSWORD')
USER = os.getenv('USER')
HOST = os.getenv('HOST')

engine = create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}:5432/postgres")

st.set_page_config(page_title="Despesas Pessoais")

with st.container():
    st.title("Despesas Pessoais")

with st.container():
    st.write("---")
    dados = pd.read_sql_table('despesas', con=engine)
    st.line_chart(dados, x="date", y="moradia")

with st.container():
    st.write("---")
    col1, col2 = st.columns(2)
    with col1:
        despesa_moradia = st.number_input('Moradia:', 0.0, 9999.0)
        #v2 = st.number_input('Saúde:', 0.0, 9999.0)
        #v3 = st.number_input('Alimentação:', 0.0, 9999.0)
        #v4 = st.number_input('Educação:', 0.0, 9999.0)
        #v5 = st.number_input('Transporte:', 0.0, 9999.0)
        #v6 = st.number_input('Gastos Pessoais:', 0.0, 9999.0)
        #v6 = st.number_input('Diversão:', 0.0, 9999.0)

    with col2:
        d_despesa_moradia = {"Aluguel": 0, "Luz": 1, "Água": 2}

        sbox1 = st.selectbox(" ", ["Aluguel","Luz","Água"])
        sg_despesa_moradia = d_despesa_moradia[sbox1]
        print(sg_despesa_moradia)

with st.container():
    button1 = st.button("Enviar", 1)
    if button1:
        grava_dados_postgres(despesa_moradia, sg_despesa_moradia)
