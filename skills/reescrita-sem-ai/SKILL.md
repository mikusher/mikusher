---
name: reescrita-sem-ai
description: Reescreva texto para remover padrões típicos de escrita de IA e preservar a voz humana do autor. Use quando o utilizador pedir texto "humanizado", "menos ChatGPT", "menos robótico", "sem sinais de IA", "AI-free", ou quando disser que o rascunho veio de uma IA.
---

# Reescrita sem IA

Reescreva o conteúdo para soar como texto produzido por uma pessoa bem-informada, removendo os padrões catalogados em `references/signs.md`.

Antes da primeira reescrita numa conversa, leia `references/signs.md`. Essa referência define os sinais e as correções preferidas.

## Princípio

Os sinais são sintomas, não uma lista de palavras proibidas. Não troque apenas uma palavra por um sinónimo. Corrija o problema da frase: exagero, generalidade, contraste artificial, ritmo mecânico, atribuição vaga, tom promocional, estrutura demasiado simétrica ou restos de linguagem de chatbot.

O objetivo é texto claro, específico e natural.

## Fluxo de trabalho

1. Obtenha o texto.
2. Leia `references/signs.md`.
3. Se houver execução de código disponível, use:
   ```bash
   python3 scripts/check_ai_signs.py <file(s)>
   python3 scripts/check_ai_signs.py <file> --summary
   ```
4. Faça também uma leitura manual para sinais que regex não deteta bem, sobretudo regra de três, variação elegante, estrutura exagerada, tom promocional e finais resumidos.
5. Reescreva frase a frase.
6. Reescaneie e releia.
7. Entregue primeiro o texto final. Se útil, acrescente uma nota curta com a contagem antes → depois, dois ou três exemplos representativos e qualquer ocorrência mantida de propósito.

## Regras obrigatórias

- Preserve factos, números, nomes, datas, links e afirmações factuais.
- Não invente factos para substituir linguagem vaga ou promocional.
- Preserve pessoa gramatical, ortografia, tom, formato e limites de comprimento.
- Nunca altere citações reais, títulos de obras, nomes próprios ou texto legal.
- Prefira frases simples com "é", "são", "tem", "usou", "escreveu", "moveu", "antes" e "para" quando forem naturais.
- Travessões longos devem ser substituídos por pontuação normal ou por uma reformulação da frase. Um uso ocasional num texto longo é aceitável.
- Remova contrastes artificiais como "não é apenas X, é Y" quando não existe uma conceção errada real a corrigir.
- Remova frases de importância abstrata quando não acrescentam factos.
- Nomeie fontes concretas quando o original as fornece. Não transforme uma fonte numa alegação vaga de "especialistas" ou "estudos".
- Se algo é desconhecido, diga-o uma vez de forma concreta. Não preencha a lacuna com especulação.
- Não acrescente "Espero que ajude", "Claro!", "Ótima pergunta", "Em conclusão", "No geral" ou outros restos de interação de chatbot.
- Não prometa que o texto é "indetetável por IA". Detetores de IA são pouco fiáveis. O objetivo é remover padrões estilísticos associados a texto gerado por LLMs.

## Sinais prioritários

Consulte `references/signs.md` para o catálogo completo. Os grupos principais são:

- importância exagerada, legado e tendências amplas;
- notabilidade enlatada e cobertura de media;
- análise superficial em cláusulas de particípio;
- tom promocional;
- atribuições vagas;
- fórmulas "desafios e perspetivas futuras";
- vocabulário de IA em alta densidade;
- evitar "é", "são" e "tem";
- associações vagas;
- paralelismos negativos;
- regra de três;
- variação elegante de sinónimos;
- títulos e formatação mecânicos;
- uso excessivo de travessões;
- emojis decorativos;
- pequenas tabelas desnecessárias;
- restos de chatbot;
- placeholders;
- "é importante notar";
- finais que apenas repetem o texto.

## Critério de saída

A melhor reescrita mantém o conteúdo e a voz, mas parece ter sido escrita diretamente por alguém que sabe exatamente o que quer dizer.