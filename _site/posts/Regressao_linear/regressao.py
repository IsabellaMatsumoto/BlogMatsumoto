import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

# Lê os dados dos arquivos
x = np.loadtxt('x.txt')
y = np.loadtxt('y.txt')

# Ajusta o formato dos dados
x = x.reshape(-1, 1)

# Cria e treina o modelo de regressão
modelo = LinearRegression()
modelo.fit(x, y)

# Faz previsões
y_pred = modelo.predict(x)

# Exibe os coeficientes
a = modelo.coef_[0]
b = modelo.intercept_
print(f"Equação da reta: y = {a:.4f}x + {b:.4f}")

# Cria o gráfico interativo
fig = go.Figure()

# Adiciona os pontos reais
fig.add_trace(go.Scatter(
    x=x.flatten(), y=y,
    mode='markers',
    name='Pontos reais',
    marker=dict(color='blue', size=8)
))

# Adiciona a reta de regressão
fig.add_trace(go.Scatter(
    x=x.flatten(), y=y_pred,
    mode='lines',
    name='Reta de regressão',
    line=dict(color='red', width=2)
))

# Configura layout
fig.update_layout(
    title='Regressão Linear',
    xaxis_title='X',
    yaxis_title='Y',
    template='plotly_white'
)

# Salva o gráfico em HTML
fig.write_html('grafico.html')
