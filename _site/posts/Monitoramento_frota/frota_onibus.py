import os
import requests
import folium
from dotenv import load_dotenv

load_dotenv(".env")
TOKEN = os.getenv("SPTRANS_TOKEN")

s = requests.Session()
auth = s.post(f"http://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar?token={TOKEN}")

if auth.text.lower() != "true":
    print("Falha na autenticação com o token SPTrans.")
    exit()

linha_nome = "875A"
url_linhas = f"http://api.olhovivo.sptrans.com.br/v2.1/Linha/Buscar?termosBusca={linha_nome}"
res_linhas = s.get(url_linhas)
linhas = res_linhas.json()

if not linhas:
    print("Nenhuma linha encontrada.")
    exit()

#Exibe as direções disponíveis 
for i, l in enumerate(linhas, start=1):
    sentido = "Ida" if l["sl"] == 1 else "Volta"
    print(f"{i}. {l['lt']} - {l['tp']} → {l['ts']} ({sentido}) | Código: {l['cl']}")


linha = linhas[0]
codigo_linha = linha["cl"]
sentido = linha["sl"]

print(f"\nLinha selecionada: {linha['lt']} - {linha['tp']} → {linha['ts']} ({'Ida' if sentido == 1 else 'Volta'})")

# Buscar paradas da linha 
url_paradas = f"http://api.olhovivo.sptrans.com.br/v2.1/Parada/BuscarParadasPorLinha?codigoLinha={codigo_linha}&sentido={sentido}"
res_paradas = s.get(url_paradas)
paradas = res_paradas.json()

if not paradas:
    print("Nenhuma parada encontrada para esta linha e sentido.")
    exit()

# Criação do mapa 
mapa = folium.Map(location=[paradas[0]["py"], paradas[0]["px"]], zoom_start=13)

# Pinos azuis = paradas
for parada in paradas:
    folium.Marker(
        [parada["py"], parada["px"]],
        popup=parada["np"],
        icon=folium.Icon(color="blue", icon="bus", prefix="fa")
    ).add_to(mapa)

# Posições em tempo real 
url_posicoes = f"http://api.olhovivo.sptrans.com.br/v2.1/Posicao?codigoLinha={codigo_linha}"
res_posicoes = s.get(url_posicoes)
dados_posicao = res_posicoes.json()

veiculos = []
if dados_posicao and "vs" in dados_posicao:
    veiculos = dados_posicao["vs"]


if veiculos:
    for v in veiculos:
        folium.Marker(
            [v["py"], v["px"]],
            popup=f"Ônibus {v['p']}",
            icon=folium.Icon(color="red", icon="location-dot", prefix="fa")
        ).add_to(mapa)
else:
    print(" Nenhum ônibus encontrado em tempo real no momento.")

#Linha 875A-10 - VILA MARIANA ↔ AEROPORTO (CONGONHAS)
mapa.save("mapa_frota_875A-10.html")

