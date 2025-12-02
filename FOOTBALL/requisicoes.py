import requests
import json
import datetime

BASE_URL = 'https://api.football-data.org/v4/matches'
headers = { 'X-Auth-Token': '5514ffb610b34325a18841e2f81456fa' }

""" uri = 'https://api.football-data.org/v4/matches'
headers = { 'X-Auth-Token': '5514ffb610b34325a18841e2f81456fa' }

response = requests.get(uri, headers=headers)
for match in response.json()['matches']:
    print (match)
 """
def buscar_id(nome_time):
    # Ceará SC joga na Série B Brasileira (ID: 2013)
    uri = 'http://api.football-data.org/v4/competitions/2013/teams'
    response = requests.get(uri, headers=headers)
    
    if response.status_code == 200:
        for team in response.json()['teams']:
            if nome_time.lower() in team['name'].lower():
                print(f"Nome: {team['name']}")
                print(f"ID: {team['id']}")
                print(f"Nome curto: {team['shortName']}")
                print(f"Sigla: {team['tla']}")
                print("---")
    else:
        print(f"Erro: {response.status_code}")
        print(response.json())

#buscar_id('Ceará')

def listar_historico_ceara():
    #id do ceará: 1837
    uri = 'http://api.football-data.org/v4/teams/1837/matches?status=FINISHED'

    response = requests.get(uri, headers=headers)
    jogos_ceara= []
    for match in response.json()['matches']:
        data = datetime.datetime.strptime(match['utcDate'][:10], '%Y-%m-%d').strftime('%d/%m/%Y')

        if match['homeTeam']['name']=='Ceará SC':
            local='Casa'
            adversario=match['awayTeam']['name']
            gols_pro=match['score']['fullTime']['home']
            gols_contra=match['score']['fullTime']['away']
        else:
            local='Fora'
            adversario=match['homeTeam']['name']
            gols_pro=match['score']['fullTime']['away']
            gols_contra=match['score']['fullTime']['home']
            
            #jogos_ceara= match['competition']['name'], ' Data: ' + match['utcDate'][:10],match['homeTeam']['name'] + ' - ' + str(match['score']['fullTime']['home']) + ' x '+ match['awayTeam']['name']+' - '+ str(match['score']['fullTime']['away'])
        
        jogos_ceara.append(f"{data} | {local:4} | Ceará - {gols_pro} vs {adversario:30} - {gols_contra}")

    return jogos_ceara

def proximos_jogos_ceara():
    uri = 'http://api.football-data.org/v4/teams/1837/matches?status=SCHEDULED'
    response = requests.get(uri, headers=headers)
    schedule_ceara=[]
    for match in response.json()['matches']:
        if match['homeTeam']['name']=='Ceará SC':
            local='Casa'
            adversario=match['awayTeam']['name']
        else:
            local='Fora'
            adversario=match['homeTeam']['name']
        schedule_ceara.append(f"{match['utcDate'][:10]} | {local:4} | Ceará vs {adversario:30}")
    return schedule_ceara


def escalacao():
    uri = 'http://api.football-data.org/v4/teams/1837'
    
    response = requests.get(uri, headers=headers)
    
    if response.status_code == 200:
        dados = response.json()
        
        escalacao_info = {
            'time': dados['name'],
            'tecnico': dados.get('coach', {}).get('name', 'Não disponível'),
            'jogadores': []
        }
        
        # Organizar jogadores por posição
        for jogador in dados.get('squad', []):
            escalacao_info['jogadores'].append({
                'nome': jogador['name'],
                'posicao': jogador['position'],
                'nacionalidade': jogador.get('nationality', 'N/A'),
                'idade': calcular_idade(jogador.get('dateOfBirth', ''))
            })
        
        return escalacao_info
    else:
        return None

def calcular_idade(data_nascimento):
    if not data_nascimento:
        return 'N/A'
    try:
        nascimento = datetime.datetime.strptime(data_nascimento, '%Y-%m-%d')
        hoje = datetime.datetime.now()
        idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
        return idade
    except:
        return 'N/A'