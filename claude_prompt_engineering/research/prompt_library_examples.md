# Exemplos e Análise de Bibliotecas de Prompts Oficiais da Anthropic

## Prompt Generator

A Anthropic oferece um gerador de prompts oficial que ajuda a criar templates de alta qualidade para tarefas específicas. Este gerador:

- É compatível com todos os modelos Claude, incluindo aqueles com capacidades de pensamento estendido
- Segue as melhores práticas de engenharia de prompts da Anthropic
- Serve como ponto de partida para testes e iterações posteriores
- Está disponível diretamente no Console da Anthropic e como notebook Colab

## Biblioteca de Prompts

A Anthropic mantém uma biblioteca de prompts otimizados para diversos casos de uso, organizados por categorias:

### Exemplos de Personas Especializadas

1. **Excel Formula Expert**
   - Persona especializada em criar fórmulas do Excel com base em descrições de usuários
   - Estrutura clara com sistema e exemplo de interação
   - Abordagem passo a passo para explicar componentes complexos

2. **Corporate Clairvoyant**
   - Especializado em extrair insights de relatórios corporativos longos
   - Foco em identificação de riscos e destilação de informações-chave

3. **Website Wizard**
   - Criação de websites de página única com base em especificações do usuário
   - Combina design e funcionalidade

### Estrutura Comum dos Prompts

Analisando os exemplos da biblioteca oficial, identificamos uma estrutura comum:

1. **Definição clara da persona/especialidade**
   - "Como um Excel Formula Expert, sua tarefa é..."
   - Define o escopo e expertise específica

2. **Instruções para coleta de informações**
   - "Certifique-se de reunir todas as informações necessárias..."
   - Orienta o modelo a solicitar detalhes quando necessário

3. **Processo de trabalho estruturado**
   - "Uma vez que você tenha um entendimento claro dos requisitos do usuário..."
   - Define etapas claras para o modelo seguir

4. **Formato de saída esperado**
   - "Forneça uma explicação detalhada da fórmula do Excel..."
   - Especifica como o resultado deve ser apresentado

5. **Contexto adicional e dicas**
   - "Além disso, forneça qualquer contexto necessário ou dicas..."
   - Incentiva o modelo a fornecer informações complementares úteis

## Padrões de Parametrização

Os prompts oficiais da Anthropic frequentemente incluem:

1. **Parâmetros de personalidade**
   - Tom de comunicação (técnico, amigável, formal)
   - Nível de detalhe nas explicações

2. **Parâmetros de formato**
   - Estrutura da resposta (passo a passo, resumida, detalhada)
   - Uso de formatação específica (markdown, HTML, etc.)

3. **Parâmetros de processo**
   - Como lidar com informações incompletas
   - Quando solicitar esclarecimentos

## Considerações para Múltiplos Modelos de IA

Para garantir compatibilidade com múltiplos modelos de IA (não apenas Claude), os prompts devem:

1. **Evitar referências específicas ao Claude**
   - Usar termos genéricos como "você" em vez de "Claude"

2. **Minimizar dependência de recursos exclusivos**
   - Estruturar prompts para funcionarem mesmo sem recursos como "pensamento estendido"

3. **Usar formatação universal**
   - Preferir marcações amplamente suportadas (markdown básico)
   - Oferecer alternativas para tags XML quando necessário

4. **Parametrizar limites de contexto**
   - Ajustar expectativas de comprimento com base no modelo alvo

5. **Considerar diferenças de treinamento**
   - Ajustar referências temporais com base nas datas de corte de treinamento
   - Evitar pressupostos sobre conhecimentos específicos
