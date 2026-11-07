from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

PASTA = Path(__file__).parent
ARQUIVO_CSV = PASTA / "casos_aws.csv"
ARQUIVO_ESTILO = PASTA / "estilo.mplstyle"

CORES = {
    "Amazon S3": "#FF4FA3",   # rosa
    "Amazon EC2": "#A855F7",  # roxo
    "Amazon RDS": "#4D7CFF",  # azul
}

def aplicar_estilo():
    """Usa o estilo escuro do projeto, se o arquivo existir."""
    if ARQUIVO_ESTILO.exists():
        plt.style.use(ARQUIVO_ESTILO)


def carregar_dados(caminho):
    """Lê o CSV e confere se as colunas necessárias existem."""
    df = pd.read_csv(caminho)
    obrigatorias = {"Servico", "Empresa", "Indicador", "Reducao_Percentual", "Tipo_Valor"}
    faltando = obrigatorias - set(df.columns)
    if faltando:
        raise ValueError(f"Colunas ausentes no CSV: {sorted(faltando)}")
    return df


def rotulo_valor(linha):
    """Mostra 'até 75%' quando a empresa divulgou um valor máximo."""
    prefixo = "até " if linha["Tipo_Valor"] == "ate" else ""
    return f"{prefixo}{linha['Reducao_Percentual']}%"


def grafico_casos(df):
    """Gráfico 1: um caso por barra, agrupado por serviço."""
    df = df.sort_values(["Servico", "Reducao_Percentual"], ascending=[False, True])
    nomes = df["Empresa"] + " - " + df["Indicador"]

    fig, ax = plt.subplots(figsize=(11, 6))
    barras = ax.barh(nomes, df["Reducao_Percentual"], color=df["Servico"].map(CORES))

    for barra, (_, linha) in zip(barras, df.iterrows()):
        ax.text(barra.get_width() + 1, barra.get_y() + barra.get_height() / 2,
                rotulo_valor(linha), va="center", fontsize=9)

    ax.set_xlim(0, 100)
    ax.set_xlabel("Redução informada pela empresa (%)")
    ax.set_title("Casos de redução de custo com S3, EC2 e RDS")
    legenda = [plt.Rectangle((0, 0), 1, 1, color=cor) for cor in CORES.values()]
    ax.legend(legenda, CORES.keys(), loc="upper right")
    fig.tight_layout()
    return fig


def grafico_faixa(df):
    """Gráfico 2: menor e maior redução encontrada em cada serviço."""
    faixa = df.groupby("Servico")["Reducao_Percentual"].agg(["min", "max"])
    faixa = faixa.reindex(list(CORES))

    fig, ax = plt.subplots(figsize=(9, 3.5))
    for posicao, (servico, linha) in enumerate(faixa.iterrows()):
        ax.hlines(posicao, linha["min"], linha["max"], color=CORES[servico], linewidth=8)
        ax.text(linha["min"] - 1.5, posicao, f"{linha['min']}%", ha="right", va="center", fontsize=9)
        ax.text(linha["max"] + 1.5, posicao, f"{linha['max']}%", ha="left", va="center", fontsize=9)

    ax.set_yticks(range(len(faixa)))
    ax.set_yticklabels(faixa.index)
    ax.set_xlim(0, 100)
    ax.set_xlabel("Menor e maior redução entre os casos (%)")
    ax.set_title("Faixa de redução por serviço")
    ax.invert_yaxis()
    fig.tight_layout()
    return fig


def imprimir_resumo(df):
    """Mostra no terminal cada caso com o indicador e a base de comparação."""
    print("\nCasos analisados:\n")
    for _, linha in df.iterrows():
        print(f"{linha['Servico']} | {linha['Empresa']}: {rotulo_valor(linha)} "
              f"- {linha['Indicador']} (base: {linha['Base_Comparacao']})")


def main():
    try:
        df = carregar_dados(ARQUIVO_CSV)
    except FileNotFoundError:
        raise SystemExit(f"Arquivo {ARQUIVO_CSV.name} não encontrado. Coloque-o na mesma pasta do app.py.")

    imprimir_resumo(df)
    aplicar_estilo()

    grafico_casos(df).savefig(PASTA / "grafico_casos.png", dpi=150)
    grafico_faixa(df).savefig(PASTA / "grafico_faixa.png", dpi=150)
    print("\nGráficos salvos: grafico_casos.png e grafico_faixa.png")

    plt.show()

if __name__ == "__main__":
    main()