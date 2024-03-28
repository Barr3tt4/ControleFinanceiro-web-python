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

with st.container(): #Moradia
    st.write("---")
    st.subheader("Moradia")
    st.write(" ")
    dados_moradia= pd.read_sql_table('despesas', con=engine, columns=['date_time', 'moradia'])
    dados_moradia= dados_moradia.groupby(dados_moradia.date_time.dt.date)[['moradia']].sum().reset_index()
    print(dados_moradia)
    st.line_chart(dados_moradia, x='date_time', y="moradia")

with st.container():
    st.write("---")
    st.subheader("Gastos totais do mês")
    dados_totais = pd.read_sql_table('despesas', con=engine)
    dados_totais = dados_totais.groupby(dados_totais.date_time.dt.isocalendar().week)[['moradia', 'saude', 'educacao']].sum().reset_index()
    print(dados_totais)
    st.bar_chart(dados_totais, x='week', y=['moradia', 'saude', 'educacao'])

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
