import requests
import json
import datetime 
import streamlit as st
import requisicoes
from requisicoes import listar_historico_ceara


BASE_URL = 'https://api.football-data.org/v4/matches'
HEADERS = { 'X-Auth-Token': '5514ffb610b34325a18841e2f81456fa' }

st.title('Histórico de Jogos do Ceará SC')
historico = requisicoes.listar_historico_ceara()

with st.expander('Clique para ver o histórico completo da temporada'):
    for jogo in historico:
        st.write(jogo)