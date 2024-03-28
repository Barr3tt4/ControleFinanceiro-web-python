import streamlit as st
import pandas as pd
#import os
#from dotenv import load_dotenv
from sqlalchemy import create_engine
from postgresql_con import *

load_dotenv()

PASSWORD = os.getenv('PASSWORD')
USER = os.getenv('USER')
HOST = os.getenv('HOST')

engine = create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}:5432/postgres")

st.set_page_config(
    page_title=" ",
    initial_sidebar_state="collapsed"
)

with st.container(): #sidebar

    st.sidebar.header('Insira suas despesas pessoais')
    in_desp_moradia = st.sidebar.number_input('Moradia:', 0.0, 9999.0)
    in_desp_saude = st.sidebar.number_input('Saúde:', 0.0, 9999.0)
    in_desp_alimentacao = st.sidebar.number_input('Alimentação:', 0.0, 9999.0)
    in_desp_educacao = st.sidebar.number_input('Educação:', 0.0, 9999.0)
    in_desp_transporte = st.sidebar.number_input('Transporte:', 0.0, 9999.0)
    in_desp_gastos_pessoais = st.sidebar.number_input('Gastos Pessoais', 0.0, 9999.0)
    in_desp_diversao = st.sidebar.number_input('Diversão:', 0.0, 9999.0)

    st.sidebar.write(" ")

    button1 = st.sidebar.button("Enviar", 1)
    if button1:
        grava_dados_postgres(
            in_desp_moradia,
            in_desp_saude,
            in_desp_alimentacao,
            in_desp_educacao,
            in_desp_transporte,
            in_desp_gastos_pessoais,
            in_desp_diversao
        )

#with st.container():
#    st.title("Despesas Pessoais")

with st.container():
    st.write("---")
    selecao_despesa = st.selectbox(" ", ['moradia',
                                         'saude',
                                         'alimentacao',
                                         'educacao',
                                         'transporte',
                                         'gastos_pessoais',
                                         'diversao']
                                   )
    st.write("---")
    st.subheader(f'{selecao_despesa}')
    st.write(" ")
    dados= pd.read_sql_table('despesas', con=engine, columns=['date_time', f'{selecao_despesa}'])
    dados= dados.groupby(dados.date_time.dt.date)[[f'{selecao_despesa}']].sum().reset_index()
    print(dados)
    st.line_chart(dados, x='date_time', y=f'{selecao_despesa}')

with st.container():
    st.write("---")
    st.subheader("Gastos totais (semana)")
    dados_totais = pd.read_sql_table('despesas', con=engine)
    dados_totais = dados_totais.groupby(dados_totais.date_time.dt.isocalendar().week)[['moradia',
                                                                                       'saude',
                                                                                       'alimentacao',
                                                                                       'educacao',
                                                                                       'transporte',
                                                                                       'gastos_pessoais',
                                                                                       'diversao']].sum().reset_index()
    print(dados_totais)
    st.bar_chart(dados_totais, x='week', y=['moradia',
                                            'saude',
                                            'alimentacao',
                                            'educacao',
                                            'transporte',
                                            'gastos_pessoais',
                                            'diversao'])