import numpy as np
import plotly.graph_objects as go

# Ler os dados dos arquivos
X = np.loadtxt("x.txt")  # anos de estudo
y = np.loadtxt("y.txt")  # salário

# Montar a matriz X com coluna de 1s
X_matriz = np.column_stack((np.ones(len(X)), X))

# Calcular os coeficientes a e b com a fórmula matricial
beta = np.linalg.inv(X_matriz.T @ X_matriz) @ X_matriz.T @ y
a, b = beta[0], beta[1]

print(f"a (intercepto): {a:.4f}")
print(f"b (inclinação): {b:.4f}")

# Calcular valores previstos (reta estimada)
y_pred = a + b * X

# Calcular o R² (coeficiente de determinação)
ss_res = np.sum((y - y_pred) ** 2)
ss_tot = np.sum((y - np.mean(y)) ** 2)
r2 = 1 - (ss_res / ss_tot)

print(f"R²: {r2:.4f}")

# Criar o gráfico com Plotly
fig = go.Figure()

# Pontos reais
fig.add_trace(go.Scatter(
    x=X, y=y,
    mode="markers",
    name="Dados reais",
    marker=dict(color="blue", size=8)
))

# Reta estimada
fig.add_trace(go.Scatter(
    x=X, y=y_pred,
    mode="lines",
    name="Reta estimada",
    line=dict(color="red", width=3)
))

# Layout do gráfico
fig.update_layout(
    title=f"Relação entre Anos de Estudo e Salário<br>a={a:.4f}, b={b:.4f}, R²={r2:.4f}",
    xaxis_title="Anos de Estudo",
    yaxis_title="Salário (R$)",
    template="plotly_white"
)

# Salvar o gráfico em HTML
fig.write_html("regressao_linear.html")
print("Gráfico salvo como regressao_linear.html — abra no navegador para visualizar.")
