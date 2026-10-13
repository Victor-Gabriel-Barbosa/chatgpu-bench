import json
import os


def salvar_vram(caminho_completo, valor_gb):
  """Injeta a métrica de VRAM no arquivo JSON exportado."""
  nome_arquivo = os.path.basename(caminho_completo)
  
  if valor_gb is None or not os.path.exists(caminho_completo):
    print(f"Não foi possível modificar {nome_arquivo}. VRAM capturado: {valor_gb}, Arquivo existe: {os.path.exists(caminho_completo)}")
    return

  try:
    with open(caminho_completo, 'r', encoding='utf-8') as f:
      dados = json.load(f)
    
    # Injeta a métrica de VRAM na resposta do assistente
    if "messages" in dados and len(dados["messages"]) > 0:
      ultima_msg = dados["messages"][-1]
      if "metrics" in ultima_msg:
        ultima_msg["metrics"]["vram_gb"] = valor_gb
      else:
        ultima_msg["metrics"] = {"vram_gb": valor_gb}
    
    # Sobrescreve o arquivo com os dados atualizados
    with open(caminho_completo, 'w', encoding='utf-8') as f:
      json.dump(dados, f, ensure_ascii=False, indent=2)
          
  except (OSError, json.JSONDecodeError, UnicodeDecodeError) as e:
    print(f"Erro ao atualizar JSON {nome_arquivo}: {e}")