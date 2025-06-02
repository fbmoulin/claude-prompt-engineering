# Guia de Uso do Agente de Criação de Prompts

Este guia explica como utilizar o Agente de Criação de Prompts para gerar prompts otimizados para modelos de IA, com foco especial nos modelos Claude 3.7 e Claude 4 da Anthropic, mas com suporte extensível a outros modelos.

## Estrutura de Diretórios

```
claude_prompt_engineering/
├── research/                # Documentação e pesquisa
│   ├── claude4_best_practices.md
│   ├── claude_models_parameters.md
│   └── prompt_library_examples.md
├── resources/               # Recursos para o gerador de prompts
│   ├── models.json          # Definições de modelos de IA
│   ├── personas.json        # Personas especializadas
│   └── templates.json       # Templates de estrutura de prompts
├── scripts/                 # Scripts executáveis
│   ├── prompt_generator.py  # Script principal para geração de prompts
│   └── validate_prompt_generator.py  # Script de validação
├── output/                  # Diretório para prompts gerados
└── examples/                # Exemplos de prompts gerados
```

## Requisitos

- Python 3.6 ou superior
- Não são necessárias bibliotecas externas

## Como Usar o Gerador de Prompts

1. Navegue até o diretório de scripts:
   ```
   cd claude_prompt_engineering/scripts
   ```

2. Execute o script principal:
   ```
   python3 prompt_generator.py
   ```

3. Siga as instruções interativas:
   - Selecione o modelo de IA alvo
   - Escolha uma persona especializada
   - Selecione um template de estrutura
   - Descreva a tarefa específica
   - Defina parâmetros adicionais
   - Opcionalmente, forneça exemplos

4. O prompt gerado será exibido na tela e salvo automaticamente no diretório `output/` em formato JSON.

## Personalização

### Adicionando Novos Modelos

Edite o arquivo `resources/models.json` para adicionar definições de novos modelos de IA, seguindo a estrutura existente:

```json
{
  "modelo-id": {
    "name": "Nome do Modelo",
    "description": "Descrição do modelo",
    "provider": "Nome do Provedor",
    "context_window": 32000,
    "max_output": 4000,
    "features": {
      "extended_thinking": true,
      "vision": true,
      "multilingual": true
    },
    "prompt_format": {
      "system": "system",
      "user": "user",
      "assistant": "assistant"
    },
    "training_cutoff": "YYYY-MM"
  }
}
```

### Adicionando Novas Personas

Edite o arquivo `resources/personas.json` para adicionar novas personas especializadas:

```json
{
  "persona-id": {
    "name": "Nome da Persona",
    "description": "Descrição da especialidade",
    "expertise": ["Área 1", "Área 2", "Área 3"],
    "tone": "Tom de comunicação",
    "detail_level": "Nível de detalhe",
    "approach": "Abordagem para resolução de problemas",
    "system_prompt_template": "Template do prompt de sistema para esta persona..."
  }
}
```

### Adicionando Novos Templates

Edite o arquivo `resources/templates.json` para adicionar novos templates de estrutura:

```json
{
  "template-id": {
    "name": "Nome do Template",
    "description": "Descrição do template",
    "task_type": "Tipo de Tarefa",
    "structure": {
      "introduction": "Você {ação} sobre {topic}.",
      "information_gathering": "Instruções para coleta de informações...",
      "process": "Processo de trabalho...",
      "output_format": "Formato de saída esperado...",
      "additional_context": "Contexto adicional..."
    },
    "example_input": "Exemplo de entrada",
    "example_output": "Exemplo de saída"
  }
}
```

## Validação

Para verificar se o gerador de prompts está funcionando corretamente:

```
python3 validate_prompt_generator.py
```

Este script executa testes automatizados para garantir que:
- Os arquivos de recursos são carregados corretamente
- Os prompts são gerados com a estrutura esperada
- A compatibilidade com múltiplos modelos é mantida

## Melhores Práticas

1. **Personas Específicas**: Crie personas altamente especializadas para tarefas específicas, em vez de personas genéricas.

2. **Instruções Claras**: Inclua instruções detalhadas sobre o processo de trabalho e o formato de saída esperado.

3. **Exemplos Concretos**: Forneça exemplos de entrada e saída para guiar o modelo.

4. **Parâmetros Contextuais**: Ajuste parâmetros como tom, nível de detalhe e formato de saída conforme o caso de uso.

5. **Compatibilidade Multi-modelo**: Ao criar prompts para múltiplos modelos, considere as diferenças de capacidades e formatos.

## Recursos Adicionais

Consulte os arquivos na pasta `research/` para informações detalhadas sobre:
- Melhores práticas para prompts do Claude 4
- Parâmetros e restrições dos modelos Claude
- Exemplos e análises de bibliotecas de prompts oficiais
