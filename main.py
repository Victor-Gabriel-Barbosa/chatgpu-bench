import os
import time
import webbrowser

import pyautogui
import pyperclip

from medir_vram import get_vram_gb
from salvar_vram import salvar_vram
from src.config import altura, largura, modelos, pasta_exportacao, pause, prompts
from src.gerar_graficos import gerar_graficos_svg
from src.processar_resultados import processar_benchmarks

pyautogui.pause = pause

def esperar_modelo(): 
  while True:
    time.sleep(3)
    pyautogui.hotkey("ctrl", "a")
    pyautogui.hotkey("ctrl", "c")
    time.sleep(1)
    if "Carregando modelo..." not in pyperclip.paste():
      break

def main():
  # Abre o navegador pelo executar
  webbrowser.open("https://chatgpu-nu.vercel.app/")

  # Tempo de espera para o carregamento do modelo selecionado
  esperar_modelo()

  # Ativa tela cheia
  pyautogui.click(largura // 2, altura // 2)
  time.sleep(1)
  pyautogui.press("f11")
  time.sleep(2)

  # Itera sobre cada modelo
  for modelo in modelos:
    # Inicia um novo chat
    pyautogui.click(1, 1)
    pyautogui.press("tab", presses=3)
    pyautogui.press("enter")
    time.sleep(1)
    
    # Abre o menu de seleção de modelos
    pyautogui.click(largura, 1)
    pyautogui.press("tab", presses=3)
    pyautogui.press("enter")
    time.sleep(1)
    
    # Seleciona o modelo atual dinamicamente
    pyautogui.press("tab")
    pyautogui.write(modelo, interval=0.03)
    pyautogui.press("tab", presses=3)
    pyautogui.press("space")
    
    # Tempo de espera para o carregamento do modelo selecionado
    esperar_modelo()
    
    # Fecha o menu de seleção de modelos
    pyautogui.press("escape")
    time.sleep(1)
    
    # Itera sobre cada um dos prompts para o modelo selecionado
    for i, texto_prompt in enumerate(prompts, start=1):
      # Inicia um novo chat
      pyautogui.click(1, 1)
      pyautogui.press("tab", presses=3)
      pyautogui.press("enter")
      time.sleep(1)
      
      # Envia o prompt atual  
      pyautogui.click(largura, 1)  
      pyautogui.press("tab")  
      pyperclip.copy(texto_prompt.strip())  
      pyautogui.hotkey("ctrl", "v")  
      time.sleep(1)  
      pyautogui.press("enter")  
      time.sleep(2)

      vram_gb = get_vram_gb()

      # Tempo de espera para a resposta do modelo 
      while True:
        time.sleep(4)
        pyautogui.press("tab")
        time.sleep(1)
        pyautogui.hotkey("ctrl", "a")
        time.sleep(1)
        pyautogui.hotkey("ctrl", "c")
        time.sleep(1)
        if "Gerando resposta..." not in pyperclip.paste():
          break
        pyautogui.hotkey("shift", "tab")

      # Exporta os resultados do modelo  
      pyautogui.click(1, 1)  
      pyautogui.press("tab", presses=5)  
      pyautogui.press("enter", presses=2)  
      time.sleep(1)

      # Monta o nome e caminho absoluto do arquivo
      nome_arquivo = f"Prompt{i} - {modelo}.json"
      caminho_completo = os.path.join(pasta_exportacao, nome_arquivo)
      
      # Salva o arquivo no caminho da pasta exportação
      pyautogui.write(nome_arquivo, interval=0.03)
      pyautogui.hotkey("ctrl", "l")  
      pyautogui.write(pasta_exportacao, interval=0.03)
      pyautogui.press("enter")
      time.sleep(1)
      pyautogui.hotkey("alt", "l") 
      time.sleep(2)

      # Adiciona o uso de VRAM no arquivo JSON exportado
      salvar_vram(caminho_completo, vram_gb)
      
  time.sleep(5)
  processar_benchmarks()
  time.sleep(5)
  gerar_graficos_svg()
  
if __name__ == "__main__":
  main()