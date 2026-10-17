import csv
import json
import os
from glob import glob

from src.config import pasta_exportacao, pasta_resultados

# Dicionário com os nomes para as métricas
METRICAS = {
  "tokensPerSecond": "Geração (tokens/s)",
  "completionTokens": "Tokens Gerados",
  "timeToFirstToken": "Tempo até o Primeiro Token (s)",
  "prefillTokensPerSecond": "Prefill (tokens/s)",
  "promptTokens": "Tokens de Entrada",
  "totalTokens": "Total de Tokens",
  "elapsedTime": "Tempo Total (s)",
  "vram_gb": "Uso de VRAM (GB)"
}

def obter_nome(chave):
  return METRICAS.get(chave, chave)

def formatar_nome_arquivo(nome):
  nome_limpo = "".join(c if c.isalnum() else "_" for c in nome)
  while "__" in nome_limpo:
    nome_limpo = nome_limpo.replace("__", "_")
  return nome_limpo.strip("_").lower()

def processar_benchmarks():
  if not os.path.exists(pasta_exportacao):
    print(f"Erro: A pasta '{pasta_exportacao}' não foi encontrada.")
    return

  arquivos_json = glob(os.path.join(pasta_exportacao, '*.json'))

  if not arquivos_json:
    print(f"Nenhum ficheiro JSON encontrado na pasta '{pasta_exportacao}'.")
    return

  os.makedirs(pasta_resultados, exist_ok=True)

  dados_completos = []
  todas_chaves_metricas = set()

  for caminho_arquivo in arquivos_json:
    nome_arquivo = os.path.basename(caminho_arquivo)

    if " - " in nome_arquivo:
      nome_modelo = nome_arquivo.split(" - ", 1)[1].replace(".json", "").strip()
    else:
      nome_modelo = nome_arquivo.replace(".json", "").strip()

    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
      try:
        dados = json.load(f)
      except json.JSONDecodeError:
        print(f"Erro ao descodificar {nome_arquivo}. Ficheiro ignorado.")
        continue

      metricas = None

      if 'messages' in dados:
        for msg in dados['messages']:
          if 'metrics' in msg:
            metricas = msg['metrics']
            break

      if metricas:
        linha = {'modelo': nome_modelo}
        linha |= metricas
        dados_completos.append(linha)

        todas_chaves_metricas.update(metricas.keys())
      else:
        print(f"Nenhuma métrica encontrada no ficheiro {nome_arquivo}.")

  if not dados_completos:
    print("Nenhuma métrica válida foi extraída dos ficheiros.")
    return

  chaves_originais = sorted(todas_chaves_metricas)
  caminho_todas_metricas = os.path.join(pasta_resultados, 'metricas.csv')

  with open(caminho_todas_metricas, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    cabecalho = ['Modelo'] + [obter_nome(k) for k in chaves_originais]
    writer.writerow(cabecalho)

    for dado in dados_completos:
      linha = [dado['modelo']] + [dado.get(k, 'N/A') for k in chaves_originais]
      writer.writerow(linha)

  print(f"Tabela gerada: {caminho_todas_metricas}")

if __name__ == "__main__":
  processar_benchmarks()