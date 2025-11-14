import requests
import pandas as pd
import plotly.express as px
import calendar
from datetime import datetime


def cotacao_dolar_periodo(mes_ano: str):
    # Converte string "MMYYYY" em datas inicial e final
    first_date = datetime.strptime(mes_ano, "%m%Y")
    last_day = calendar.monthrange(first_date.year, first_date.month)[1]

    data_inicial = first_date.strftime("%m-%d-%Y")
    data_final = first_date.replace(day=last_day).strftime("%m-%d-%Y")

    print(data_inicial, data_final)

    # Monta a URL da API
    url = (
        "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
        f"CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?"
        f"@dataInicial='{data_inicial}'&@dataFinalCotacao='{data_final}'&"
        "$top=1000&$format=json&$select=cotacaoCompra,dataHoraCotacao"
    )

    # Faz a requisição
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception("Erro ao acessar a API do Banco Central")

    dados = r.json().get("value", [])
    if not dados:
        raise Exception("Nenhum dado retornado pela API")

    # Converte para DataFrame
    df = pd.DataFrame(dados)
    df["dataHoraCotacao"] = pd.to_datetime(df["dataHoraCotacao"])
    df = df.sort_values("dataHoraCotacao")

    # Cria o gráfico
    fig = px.line(
        df,
        x="dataHoraCotacao",
        y="cotacaoCompra",
        title=f"Cotação do Dólar - {first_date.strftime('%B de %Y')}",
        labels={"dataHoraCotacao": "Data", "cotacaoCompra": "Cotação (R$)"}
    )
    fig.write_html("grafico_dolar.html")
    print("Gráfico salvo em grafico_dolar.html.")

if __name__ == "__main__":
    cotacao_dolar_periodo("082025")

