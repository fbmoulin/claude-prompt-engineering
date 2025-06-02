# Melhores Práticas para Prompts do Claude 4

## Princípios Gerais

### Seja explícito com suas instruções
- Os modelos Claude 4 respondem bem a instruções claras e explícitas
- Seja específico sobre o resultado desejado
- Usuários que desejam o comportamento "acima e além" dos modelos anteriores precisam solicitar explicitamente

### Adicione contexto para melhorar o desempenho
- Forneça contexto ou motivação por trás das instruções
- Explique ao Claude por que tal comportamento é importante
- Isso ajuda o Claude 4 a entender melhor seus objetivos e entregar respostas mais direcionadas

### Seja vigilante com exemplos e detalhes
- Os modelos Claude 4 prestam atenção a detalhes e exemplos como parte do seguimento de instruções
- Certifique-se de que seus exemplos estejam alinhados com os comportamentos que você deseja incentivar
- Minimize comportamentos que você deseja evitar

## Orientações para situações específicas

### Controle o formato das respostas
Formas eficazes de direcionar a formatação de saída nos modelos Claude 4:

1. **Diga ao Claude o que fazer em vez do que não fazer**
   - Em vez de: "Não use markdown em sua resposta"
   - Tente: "Sua resposta deve ser composta de parágrafos de prosa fluida"

2. **Use indicadores de formato XML**
   - Tente: "Escreva as seções de prosa de sua resposta em tags <paragrafos_de_prosa_fluida>"

3. **Combine o estilo do prompt com a saída desejada**
   - O estilo de formatação usado no prompt pode influenciar o estilo de resposta do Claude
   - Remover markdown do prompt pode reduzir o volume de markdown na saída

### Aproveite as capacidades de pensamento
- Claude 4 oferece capacidades de pensamento úteis para tarefas que envolvem reflexão após o uso de ferramentas ou raciocínio complexo em várias etapas
- Você pode orientar seu pensamento inicial ou intercalado para obter melhores resultados

### Otimize chamadas de ferramentas paralelas
- Os modelos Claude 4 se destacam na execução paralela de ferramentas
- Alta taxa de sucesso no uso de chamadas paralelas de ferramentas sem qualquer prompt para fazê-lo
- Um prompt menor pode aumentar esse comportamento para ~100% de taxa de sucesso

### Reduza a criação de arquivos em codificação agêntica
- Os modelos Claude 4 podem criar novos arquivos para fins de teste e iteração
- Essa abordagem permite que o Claude use arquivos como um "rascunho temporário"
- Se preferir minimizar a criação de novos arquivos, instrua o Claude a limpar depois

### Melhore a geração de código visual e frontend
- Para geração de código frontend, você pode direcionar os modelos Claude 4 para criar designs complexos, detalhados e interativos fornecendo incentivo explícito
- Melhore o desempenho de frontend do Claude em áreas específicas fornecendo modificadores e detalhes adicionais:
  - "Inclua o maior número possível de recursos e interações relevantes"
  - "Adicione detalhes cuidadosos como estados de hover, transições e micro-interações"
  - "Crie uma demonstração impressionante mostrando capacidades de desenvolvimento web"
  - "Aplique princípios de design: hierarquia, contraste, equilíbrio e movimento"

## Considerações de migração (de Sonnet 3.7 para Claude 4)

1. **Seja específico sobre o comportamento desejado**: Descreva exatamente o que você gostaria de ver na saída.

2. **Enquadre suas instruções com modificadores**: Adicionar modificadores que incentivem o Claude a aumentar a qualidade e o detalhe de sua saída pode ajudar a moldar melhor o desempenho do Claude. Por exemplo, em vez de "Crie um painel de análise", use "Crie um painel de análise. Inclua o maior número possível de recursos e interações relevantes. Vá além do básico para criar uma implementação completa."

3. **Solicite recursos específicos explicitamente**: Animações e elementos interativos devem ser solicitados explicitamente quando desejados.
