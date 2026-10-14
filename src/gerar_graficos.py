import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def gerar_graficos_svg():
  plt.rcParams['svg.fonttype'] = 'none'
  os.makedirs('./resultados/svg', exist_ok=True)
  df = pd.read_csv('./resultados/metricas.csv')
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
    caminho_svg = f'./resultados/svg/{nome_arquivo}.svg'

    plt.savefig(caminho_svg, format='svg', bbox_inches='tight', transparent=True)
    plt.close()
    print(f"Salvo em: {caminho_svg}")
    
if __name__ == "__main__":
  gerar_graficos_svg()