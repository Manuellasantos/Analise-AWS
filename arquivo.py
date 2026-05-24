import pandas as pd
import matplotlib.pyplot as plt

# Ler arquivo CSV
df = pd.read_csv("dados.csv")

print(df)

# =========================
# GRÁFICO 1
# =========================

x = range(len(df["Categoria"]))

plt.figure(figsize=(10,6))

plt.bar(
    x,
    df["Custo_Antes_AWS"],
    width=0.4,
    label="Antes da AWS",
    color="#ff69b4"
)

plt.bar(
    [i + 0.4 for i in x],
    df["Custo_Depois_AWS"],
    width=0.4,
    label="Depois da AWS",
    color="#c71585"
)

plt.xticks(
    [i + 0.2 for i in x],
    df["Categoria"],
    rotation=15
)

plt.ylabel("Custos Mensais (R$)")
plt.title("Comparação de Custos AWS")

plt.legend()

plt.tight_layout()
plt.show()

# =========================
# GRÁFICO 2
# =========================

plt.figure(figsize=(10,6))

plt.bar(
    df["Categoria"],
    df["Economia_Mensal"],
    color="#db7093"
)

plt.ylabel("Economia Mensal")
plt.title("Economia Gerada com AWS")

plt.xticks(rotation=15)

plt.tight_layout()
plt.show()