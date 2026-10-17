import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.config import pasta_resultados


def gerar_graficos_pdf():
  plt.rcParams['pdf.fonttype'] = 42
  os.makedirs(f"{pasta_resultados}/pdf", exist_ok=True)
  df = pd.read_csv(f"{pasta_resultados}/metricas.csv")
  metricas = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
  sns.set_theme(style="whitegrid")

  for metrica in metricas:
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x=metrica, y='Modelo', errorbar=None, hue='Modelo', legend=False)
    plt.title(f'Média de {metrica} por Modelo', fontsize=14, pad=15)
    plt.xlabel(metrica, fontsize=12)
    plt.ylabel('Modelo', fontsize=12)
    plt.tight_layout()

    nome_arquivo = metrica.lower().replace(' ', '_').replace('(', '').replace(')', '').replace('/', '_')
    caminho_pdf = f"{pasta_resultados}/pdf/{nome_arquivo}.pdf"

    plt.savefig(caminho_pdf, format='pdf', bbox_inches='tight', transparent=True)
    plt.close()
    print(f"Salvo em: {caminho_pdf}")
    
if __name__ == "__main__":
  gerar_graficos_pdf()