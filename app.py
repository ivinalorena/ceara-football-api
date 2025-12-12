from flask import Flask, request, render_template
import requests
from requisicoes import listar_historico_ceara, proximos_jogos_ceara, escalacao
import json
#transforma a linha em um dicionário
def parse_linha(linha):
    # Divide por '|'
    partes = linha.split("|")
    
    data = partes[0].strip()
    local = partes[1].strip()

    # Exemplo: "Ceará - 2 vs RB Bragantino - 2"
    jogo = partes[2].strip()

    # Separar times e gols
    casa, resto = jogo.split(" vs ")
    time_casa, gols_casa = casa.rsplit(" - ", 1)
    
    time_fora, gols_fora = resto.rsplit(" - ", 1)

    return {
        "data": data,
        "local": local,
        "time_casa": time_casa.strip(),
        "gols em casa": int(gols_casa),
        "time_fora": time_fora.strip(),
        "gols fora": int(gols_fora)
    }


app = Flask(__name__)

API_URL = "http://api.football-data.org/v4/teams/1837/matches?status=FINISHED"
API_KEY = "5514ffb610b34325a18841e2f81456fa"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/buscar", methods=["GET"])
def buscar():

    data = listar_historico_ceara()
    if not data:
        return "Nenhuma data selecionada."
    dados_convertidos = [parse_linha(linha) for linha in data]
    return render_template("tabela.html", dados=dados_convertidos)

@app.route("/proximosjogos", methods=["GET"])
def proximos_jogos():
    data = proximos_jogos_ceara()

    if not data:
        return render_template("historydefault.html")
    

    return render_template("proximosjogos.html",data=data)

@app.route("/escalacao", methods=["GET"])
def escalacao_ceara():
    from requisicoes import escalacao
    dados = escalacao()
    if not dados:
        return "Erro ao buscar escalação."
    return render_template("escalacao.html", dados=dados)

if __name__ == "__main__":
    app.run(debug=True)
