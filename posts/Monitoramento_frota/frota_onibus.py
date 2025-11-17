import os
import requests
import folium
from dotenv import load_dotenv

load_dotenv(".env")
TOKEN = os.getenv("SPTRANS_TOKEN")

s = requests.Session()
auth = s.post(f"http://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar?token={TOKEN}")
if auth.text.lower() != "true":
    print("Erro: Token inválido!")
    exit()

busca = "875A"
url_busca = f"http://api.olhovivo.sptrans.com.br/v2.1/Linha/Buscar?termosBusca={busca}"
linhas = s.get(url_busca).json()

# Filtrar exatamente a variante 875A-10 e sentido 1
linhas = [l for l in linhas if l.get("lt") == "875A" and l.get("tl") == 10 and l.get("sl") == 1]

if not linhas:
    print("Linha 875A-10 sentido 1 não encontrada.")
    exit()

linha = linhas[0]
codigo_linha = linha["cl"]
sentido = linha["sl"]

print(f"Linha selecionada: {linha['lt']}-{linha['tl']} | Sentido {sentido} | {linha['tp']} → {linha['ts']}")

url_paradas = (
    f"http://api.olhovivo.sptrans.com.br/v2.1/Parada/BuscarParadasPorLinha?"
    f"codigoLinha={codigo_linha}&sentido={sentido}"
)

paradas = s.get(url_paradas).json()
if not paradas:
    print("Nenhuma parada encontrada.")
    exit()

# Criar mapa centralizado na primeira parada
mapa = folium.Map(location=[paradas[0]["py"], paradas[0]["px"]], zoom_start=13)

# Pinos azuis das paradas
for p in paradas:
    folium.Marker(
        [p["py"], p["px"]],
        popup=p["np"],
        icon=folium.Icon(color="blue", icon="bus", prefix="fa")
    ).add_to(mapa)

url_posicao = f"http://api.olhovivo.sptrans.com.br/v2.1/Posicao?codigoLinha={codigo_linha}"
dados = s.get(url_posicao).json()

veiculos = []
if "l" in dados:
    for bloco in dados["l"]:
        if bloco.get("cl") == codigo_linha:
            veiculos = bloco.get("vs", [])
            break

# Adicionar ônibus em vermelho
for v in veiculos:
    folium.Marker(
        [v["py"], v["px"]],
        popup=f"Ônibus {v.get('p')} (875A-10 s1)",
        icon=folium.Icon(color="red", icon="location-dot", prefix="fa")
    ).add_to(mapa)

if not veiculos:
    print("⚠ Nenhum ônibus em tempo real encontrado no momento.")
else:
    print(f"✔ Ônibus encontrados: {len(veiculos)}")


mapa.save("mapa_875A_10.html")
print("Mapa gerado: mapa_875A")
