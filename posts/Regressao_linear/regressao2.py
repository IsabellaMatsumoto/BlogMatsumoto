import numpy as np
from plotnine import (
  ggplot, aes, geom_point, geom_smooth, geom_abline, theme, element_text, ggsave
)
import pandas as pd

# Ler os arquivos
valores_x = np.loadtxt("x.txt")
valores_y = np.loadtxt("y.txt")

# Calcular coeficientes da regressão
X = np.column_stack((np.ones(len(valores_x)), valores_x))
beta = np.linalg.inv(X.T @ X) @ X.T @ valores_y

a = float(beta[0])   # intercepto
b = float(beta[1])   # inclinação

print("a =", a)
print("b =", b)


df = {"x": valores_x, "y": valores_y}

plot = (
    ggplot(pd.DataFrame(df), aes("x", "y"))
    + geom_point()
    + geom_abline(intercept=a, slope=b)
)

# Salvar corretamente
plot.save("grafico2.png", dpi=300)

print("Gráfico salvo como grafico.png")
