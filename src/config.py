import pyautogui

pasta_exportacao = "./bench"

pause = 0.3

largura, altura = pyautogui.size()

modelos = [
  "Qwen2.5 0.5B Instruct Q4f16.1",
  "Llama 3.2 1B Instruct Q4f16.1",
  "Qwen3 1.7B Q4f16.1",
  "Gemma 2 2b It Q4f16.1 1k",
  "Llama 3.2 3B Instruct Q4f16.1",
  "Qwen3 4B Q4f16.1",
]

prompts = [
  """
  Leia o texto a seguir e extraia as informações solicitadas.

  Texto: “Marina mora em Uberlândia. Ela pediu 2 teclados, cada um por R$ 120,00, e 1 mouse por R$ 80,00. O pedido deve ter entrega prioritária.”

  Retorne somente um JSON válido, sem bloco Markdown e sem texto antes ou depois. Use exatamente esta estrutura e estes nomes de campos:
  {
    "cliente": "string",
    "cidade": "string",
    "itens": [
      {"produto": "string", "quantidade": 0, "preco_unitario": 0.00}
    ],
    "total_pedido": 0.00,
    "entrega_prioritaria": true
  }
  Use números, e não textos, nos campos numéricos. Calcule o total do pedido. Não acrescente campos.
  """,
  """
  Quatro tarefas — A, B, C e D — precisam ser executadas uma após a outra. A tarefa D deve ocorrer antes de A; A deve ocorrer antes de C; e C deve ocorrer antes de B.

  Qual é a ordem que respeita todas as condições? Responda somente com as quatro letras, separadas por setas, da primeira para a última tarefa. Não inclua explicações.
  """,
  """
  Uma papelaria comprou 24 cadernos por R$ 8,50 cada. Vendeu 15 cadernos pelo preço normal de R$ 12,00 cada e vendeu os 9 restantes com desconto de 50% sobre o preço normal.

  Calcule:
  1. O custo total da compra.
  2. A receita obtida com os 15 cadernos vendidos pelo preço normal.
  3. A receita obtida com os 9 cadernos vendidos com desconto.
  4. A receita total.
  5. O lucro final, considerando receita total menos custo total.

  Mostre a conta de cada item e o resultado em reais, com duas casas decimais. Não considere outros custos ou impostos.
  """,
  """
  Resuma o texto abaixo sem adicionar informações externas.

  Texto:
  “Executar um modelo de linguagem localmente no navegador significa baixar os arquivos do modelo e realizar a geração de respostas no próprio dispositivo, usando recursos como a GPU por meio de tecnologias web compatíveis. Essa abordagem pode reduzir a necessidade de enviar cada pergunta a um servidor remoto e pode funcionar sem uma conexão contínua depois que os arquivos necessários estiverem disponíveis. Porém, o desempenho depende do hardware, do tamanho do modelo e da memória disponível. Modelos maiores podem gerar respostas melhores em algumas tarefas, mas também podem demorar mais para iniciar, consumir mais recursos ou não funcionar em determinados dispositivos. A execução local, por si só, não garante privacidade absoluta: isso também depende de como a aplicação trata os dados e de quais serviços externos utiliza.”

  Use exatamente este formato:
  Resumo: duas frases, com no máximo 40 palavras no total.
  Pontos-chave:
  - três tópicos, cada um com no máximo 10 palavras.
  """,
  """
  Escreva uma função em TypeScript chamada `removeDuplicados` com a assinatura `function removeDuplicados(valores: string[]): string[]`.

  A função deve remover valores repetidos exatamente iguais, preservar a ordem da primeira ocorrência e não alterar as strings. Não use bibliotecas externas.

  Retorne somente código TypeScript, sem Markdown nem explicações. Inclua a função e três verificações executáveis com `console.assert` para estes casos:
  1. `['ana', 'bia', 'ana', 'caio', 'bia']` deve produzir `['ana', 'bia', 'caio']`.
  2. `[]` deve produzir `[]`.
  3. `['x']` deve produzir `['x']`.
  """,
  """
  Analise a função TypeScript a seguir:

  function calcularMedia(valores: number[]): number {
    let soma = 0;
    for (let i = 0; i <= valores.length; i++) {
      soma += valores[i];
    }
    return soma / valores.length;
  }

  A função tem problemas. Corrija-a para que calcule a média corretamente e retorne `0` quando o array estiver vazio.

  Responda usando exatamente estas seções:
  Problemas: explique brevemente os problemas encontrados.
  Código corrigido: apresente a função completa em TypeScript dentro de um bloco de código.
  Teste rápido: informe o resultado esperado para `[2, 4, 6]` e para `[]`.
  """,
]