# Parâmetros e Restrições dos Modelos Claude 3.7 e Claude 4

## Identificação dos Modelos

### Claude 4
- **Variantes**: 
  - Claude Opus 4
  - Claude Sonnet 4
- **IDs de Modelo**:
  - Claude Opus 4: `claude-opus-4-20250514`
  - Claude Sonnet 4: `claude-sonnet-4-20250514`
- **Aliases**:
  - Claude Opus 4: `claude-opus-4-0`
  - Claude Sonnet 4: `claude-sonnet-4-0`

### Claude 3.7
- **Variantes**:
  - Claude Sonnet 3.7
- **IDs de Modelo**:
  - Claude Sonnet 3.7: `claude-3-7-sonnet-20250219`
- **Aliases**:
  - Claude Sonnet 3.7: `claude-3-7-sonnet-latest`

## Capacidades e Limites

### Janelas de Contexto
- Claude Opus 4: 200K tokens
- Claude Sonnet 4: 200K tokens
- Claude Sonnet 3.7: 200K tokens

### Limites de Saída
- Claude Opus 4: 32.000 tokens
- Claude Sonnet 4: 64.000 tokens
- Claude Sonnet 3.7: 64.000 tokens (até 128K tokens com o cabeçalho beta `output-128k-2025-02-19`)

### Recursos Especiais
- **Extended Thinking**: Disponível em Claude Opus 4, Claude Sonnet 4 e Claude Sonnet 3.7
- **Visão**: Todos os modelos suportam processamento de imagens
- **Multilíngue**: Todos os modelos têm suporte multilíngue robusto

### Latência Comparativa
- Claude Opus 4: Moderadamente rápido
- Claude Sonnet 4: Rápido
- Claude Sonnet 3.7: Rápido

### Data de Corte de Treinamento
- Claude Opus 4: Março 2025
- Claude Sonnet 4: Março 2025
- Claude Sonnet 3.7: Novembro 2024 (conhecimento confiável até outubro 2024)

## Preços (por milhão de tokens)

### Claude Opus 4
- Tokens de entrada: $15/MTok
- Tokens de saída: $75/MTok
- Cache Writes (5m): $18.75/MTok
- Cache Writes (1h): $30/MTok
- Cache Hits & Refreshes: $1.50/MTok

### Claude Sonnet 4
- Tokens de entrada: $3/MTok
- Tokens de saída: $15/MTok
- Cache Writes (5m): $3.75/MTok
- Cache Writes (1h): $6/MTok
- Cache Hits & Refreshes: $0.30/MTok

### Claude Sonnet 3.7
- Tokens de entrada: $3/MTok
- Tokens de saída: $15/MTok
- Cache Writes (5m): $3.75/MTok
- Cache Writes (1h): $6/MTok
- Cache Hits & Refreshes: $0.30/MTok

## Características de Desempenho

### Claude Opus 4
- Descrição: Modelo mais capaz e inteligente
- Pontos fortes: Nível mais alto de inteligência e capacidade
- Ideal para: Tarefas complexas de raciocínio, codificação avançada

### Claude Sonnet 4
- Descrição: Modelo de alto desempenho
- Pontos fortes: Alta inteligência e desempenho equilibrado
- Ideal para: Maioria das aplicações que exigem bom equilíbrio entre desempenho e custo

### Claude Sonnet 3.7
- Descrição: Modelo de alto desempenho com pensamento estendido
- Pontos fortes: Alta inteligência com pensamento estendido ativável
- Ideal para: Tarefas que exigem reflexão profunda e raciocínio em várias etapas

## Considerações de Migração

Ao migrar de Claude 3.7 para Claude 4:

1. **Instruções mais explícitas**: Claude 4 segue instruções com mais precisão, mas pode exigir direcionamento mais explícito para comportamentos "acima e além"

2. **Modificadores de instrução**: Adicionar modificadores que incentivem o Claude a aumentar a qualidade e o detalhe de sua saída

3. **Recursos específicos**: Solicitar explicitamente recursos como animações e elementos interativos quando desejados

## Recomendações de Uso em Produção

- Use IDs de modelo específicos (ex: `claude-sonnet-4-20250514`) em vez de aliases em aplicações de produção
- Considere o uso de streaming para respostas longas para evitar timeouts
- Monitore o uso de tokens para otimização de custos
