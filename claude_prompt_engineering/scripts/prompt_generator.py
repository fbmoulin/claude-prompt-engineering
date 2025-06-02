#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gerador de Prompts para Modelos de IA
-------------------------------------

Este script interativo permite criar prompts otimizados para modelos de IA,
com foco especial nos modelos Claude 3.7 e Claude 4 da Anthropic, mas com
suporte extensível a outros modelos de IA.

Autor: Manus AI
Data: Junho 2025
"""

import os
import json
import sys
import re
from datetime import datetime
from typing import Dict, List, Optional, Union, Any

# Constantes
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "resources")
OUTPUT_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "output")

# Garantir que os diretórios existam
os.makedirs(RESOURCES_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Arquivos de recursos
PERSONAS_FILE = os.path.join(RESOURCES_DIR, "personas.json")
TEMPLATES_FILE = os.path.join(RESOURCES_DIR, "templates.json")
MODELS_FILE = os.path.join(RESOURCES_DIR, "models.json")

# Cores para terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Classe base para componentes do agente
class PromptComponent:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    def __str__(self) -> str:
        return f"{self.name}: {self.description}"

# Modelo de IA
class AIModel(PromptComponent):
    def __init__(self, name: str, description: str, provider: str, 
                 context_window: int, max_output: int, 
                 features: Dict[str, bool], 
                 prompt_format: Dict[str, str],
                 training_cutoff: str):
        super().__init__(name, description)
        self.provider = provider
        self.context_window = context_window
        self.max_output = max_output
        self.features = features
        self.prompt_format = prompt_format
        self.training_cutoff = training_cutoff

# Persona para o modelo de IA
class Persona(PromptComponent):
    def __init__(self, name: str, description: str, 
                 expertise: List[str], tone: str, 
                 detail_level: str, approach: str,
                 system_prompt_template: str):
        super().__init__(name, description)
        self.expertise = expertise
        self.tone = tone
        self.detail_level = detail_level
        self.approach = approach
        self.system_prompt_template = system_prompt_template

# Template de estrutura de prompt
class PromptTemplate(PromptComponent):
    def __init__(self, name: str, description: str, 
                 task_type: str, structure: Dict[str, str],
                 example_input: str, example_output: str):
        super().__init__(name, description)
        self.task_type = task_type
        self.structure = structure
        self.example_input = example_input
        self.example_output = example_output

# Gerenciador de recursos
class ResourceManager:
    @staticmethod
    def load_json(file_path: str, default_value: Any = None) -> Any:
        """Carrega dados de um arquivo JSON"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return default_value
        except Exception as e:
            print(f"Erro ao carregar {file_path}: {e}")
            return default_value
    
    @staticmethod
    def save_json(file_path: str, data: Any) -> bool:
        """Salva dados em um arquivo JSON"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Erro ao salvar {file_path}: {e}")
            return False
    
    @staticmethod
    def load_models() -> Dict[str, AIModel]:
        """Carrega modelos de IA disponíveis"""
        models_data = ResourceManager.load_json(MODELS_FILE, {})
        models = {}
        
        # Adicionar modelos padrão se o arquivo não existir
        if not models_data:
            models_data = {
                "claude-opus-4": {
                    "name": "Claude Opus 4",
                    "description": "Modelo mais capaz e inteligente da Anthropic",
                    "provider": "Anthropic",
                    "context_window": 200000,
                    "max_output": 32000,
                    "features": {
                        "extended_thinking": True,
                        "vision": True,
                        "multilingual": True
                    },
                    "prompt_format": {
                        "system": "system",
                        "user": "user",
                        "assistant": "assistant"
                    },
                    "training_cutoff": "2025-03"
                },
                "claude-sonnet-4": {
                    "name": "Claude Sonnet 4",
                    "description": "Modelo de alto desempenho da Anthropic",
                    "provider": "Anthropic",
                    "context_window": 200000,
                    "max_output": 64000,
                    "features": {
                        "extended_thinking": True,
                        "vision": True,
                        "multilingual": True
                    },
                    "prompt_format": {
                        "system": "system",
                        "user": "user",
                        "assistant": "assistant"
                    },
                    "training_cutoff": "2025-03"
                },
                "claude-3-7-sonnet": {
                    "name": "Claude Sonnet 3.7",
                    "description": "Modelo de alto desempenho com pensamento estendido",
                    "provider": "Anthropic",
                    "context_window": 200000,
                    "max_output": 64000,
                    "features": {
                        "extended_thinking": True,
                        "vision": True,
                        "multilingual": True
                    },
                    "prompt_format": {
                        "system": "system",
                        "user": "user",
                        "assistant": "assistant"
                    },
                    "training_cutoff": "2024-10"
                },
                "gpt-4": {
                    "name": "GPT-4",
                    "description": "Modelo avançado da OpenAI",
                    "provider": "OpenAI",
                    "context_window": 128000,
                    "max_output": 4096,
                    "features": {
                        "extended_thinking": False,
                        "vision": True,
                        "multilingual": True
                    },
                    "prompt_format": {
                        "system": "system",
                        "user": "user",
                        "assistant": "assistant"
                    },
                    "training_cutoff": "2023-04"
                },
                "gemini-pro": {
                    "name": "Gemini Pro",
                    "description": "Modelo avançado do Google",
                    "provider": "Google",
                    "context_window": 32000,
                    "max_output": 8192,
                    "features": {
                        "extended_thinking": False,
                        "vision": True,
                        "multilingual": True
                    },
                    "prompt_format": {
                        "system": "system",
                        "user": "user",
                        "assistant": "model"
                    },
                    "training_cutoff": "2023-12"
                }
            }
            ResourceManager.save_json(MODELS_FILE, models_data)
        
        # Converter dados em objetos AIModel
        for model_id, model_data in models_data.items():
            models[model_id] = AIModel(
                name=model_data.get("name", model_id),
                description=model_data.get("description", ""),
                provider=model_data.get("provider", ""),
                context_window=model_data.get("context_window", 0),
                max_output=model_data.get("max_output", 0),
                features=model_data.get("features", {}),
                prompt_format=model_data.get("prompt_format", {}),
                training_cutoff=model_data.get("training_cutoff", "")
            )
        
        return models
    
    @staticmethod
    def load_personas() -> Dict[str, Persona]:
        """Carrega personas disponíveis"""
        personas_data = ResourceManager.load_json(PERSONAS_FILE, {})
        personas = {}
        
        # Adicionar personas padrão se o arquivo não existir
        if not personas_data:
            personas_data = {
                "excel-expert": {
                    "name": "Excel Formula Expert",
                    "description": "Especialista em criar fórmulas do Excel com base em descrições de usuários",
                    "expertise": ["Excel", "Fórmulas", "Análise de dados"],
                    "tone": "Técnico mas acessível",
                    "detail_level": "Detalhado com explicações passo a passo",
                    "approach": "Analítico e explicativo",
                    "system_prompt_template": "Como um Excel Formula Expert, sua tarefa é fornecer fórmulas avançadas do Excel que realizem os cálculos ou manipulações de dados descritos pelo usuário. Se o usuário não fornecer essas informações, pergunte ao usuário para descrever o resultado desejado ou a operação que deseja realizar no Excel. Certifique-se de reunir todas as informações necessárias para escrever uma fórmula completa, como os intervalos de células relevantes, condições específicas, critérios múltiplos ou formato de saída desejado. Depois de ter uma compreensão clara dos requisitos do usuário, forneça uma explicação detalhada da fórmula do Excel que alcançaria o resultado desejado. Divida a fórmula em seus componentes, explicando o propósito e a função de cada parte e como elas funcionam juntas. Além disso, forneça qualquer contexto necessário ou dicas para usar a fórmula efetivamente dentro de uma planilha do Excel."
                },
                "legal-analyst": {
                    "name": "Analista Jurídico",
                    "description": "Especialista em análise de documentos jurídicos e contratos",
                    "expertise": ["Direito", "Contratos", "Análise de riscos"],
                    "tone": "Formal e preciso",
                    "detail_level": "Detalhado com referências específicas",
                    "approach": "Metódico e analítico",
                    "system_prompt_template": "Como um Analista Jurídico especializado, sua função é analisar documentos legais, identificar riscos potenciais e fornecer insights jurídicos precisos. Ao receber um documento ou consulta, você deve: 1) Identificar o tipo de documento e jurisdição aplicável; 2) Analisar cláusulas e termos importantes; 3) Destacar potenciais riscos ou inconsistências; 4) Sugerir melhorias ou alternativas quando apropriado; 5) Fornecer uma avaliação geral do documento. Mantenha um tom formal e preciso, com referências específicas ao texto analisado. Quando necessário, solicite informações adicionais para contextualizar sua análise. Evite dar conselhos jurídicos definitivos, mas forneça análises fundamentadas que possam auxiliar na tomada de decisões."
                },
                "code-developer": {
                    "name": "Desenvolvedor de Código",
                    "description": "Especialista em desenvolvimento de software e programação",
                    "expertise": ["Programação", "Desenvolvimento de software", "Arquitetura de sistemas"],
                    "tone": "Técnico e colaborativo",
                    "detail_level": "Código bem comentado com explicações",
                    "approach": "Prático e orientado a soluções",
                    "system_prompt_template": "Como um Desenvolvedor de Código experiente, sua tarefa é criar, revisar ou depurar código conforme solicitado pelo usuário. Ao receber uma solicitação, você deve: 1) Compreender claramente os requisitos funcionais e técnicos; 2) Escrever código limpo, eficiente e bem documentado; 3) Explicar a lógica e as decisões de implementação; 4) Fornecer comentários úteis no código; 5) Sugerir melhorias ou alternativas quando relevante. Seu código deve seguir as melhores práticas da linguagem em questão e considerar aspectos como desempenho, segurança e manutenibilidade. Se os requisitos forem ambíguos, faça perguntas para esclarecer antes de implementar a solução. Mantenha um tom técnico mas acessível, e esteja preparado para explicar conceitos complexos de forma compreensível."
                }
            }
            ResourceManager.save_json(PERSONAS_FILE, personas_data)
        
        # Converter dados em objetos Persona
        for persona_id, persona_data in personas_data.items():
            personas[persona_id] = Persona(
                name=persona_data.get("name", persona_id),
                description=persona_data.get("description", ""),
                expertise=persona_data.get("expertise", []),
                tone=persona_data.get("tone", ""),
                detail_level=persona_data.get("detail_level", ""),
                approach=persona_data.get("approach", ""),
                system_prompt_template=persona_data.get("system_prompt_template", "")
            )
        
        return personas
    
    @staticmethod
    def load_templates() -> Dict[str, PromptTemplate]:
        """Carrega templates de prompt disponíveis"""
        templates_data = ResourceManager.load_json(TEMPLATES_FILE, {})
        templates = {}
        
        # Adicionar templates padrão se o arquivo não existir
        if not templates_data:
            templates_data = {
                "qa-template": {
                    "name": "Pergunta e Resposta",
                    "description": "Template para perguntas e respostas diretas",
                    "task_type": "QA",
                    "structure": {
                        "introduction": "Você responderá perguntas sobre {topic}.",
                        "information_gathering": "Se a pergunta for ambígua ou faltar informações, peça esclarecimentos.",
                        "process": "Analise a pergunta cuidadosamente e forneça uma resposta precisa e informativa.",
                        "output_format": "Sua resposta deve ser clara, concisa e diretamente relacionada à pergunta.",
                        "additional_context": "Quando relevante, forneça contexto adicional ou exemplos para enriquecer sua resposta."
                    },
                    "example_input": "Qual é a diferença entre machine learning e deep learning?",
                    "example_output": "Machine learning e deep learning são subcampos da inteligência artificial, mas com diferenças importantes:\n\nMachine Learning:\n- Usa algoritmos que aprendem padrões a partir de dados\n- Geralmente requer engenharia de features manual\n- Inclui algoritmos como regressão, árvores de decisão e SVM\n- Funciona bem com conjuntos de dados menores\n\nDeep Learning:\n- Subconjunto do machine learning baseado em redes neurais artificiais\n- Realiza extração automática de features\n- Utiliza redes neurais com múltiplas camadas (profundas)\n- Geralmente requer grandes volumes de dados\n- Excele em tarefas complexas como visão computacional e processamento de linguagem natural\n\nEm resumo, deep learning é um tipo especializado de machine learning que usa redes neurais profundas e geralmente oferece maior poder preditivo para problemas complexos, mas com maior custo computacional e necessidade de dados."
                },
                "code-generation": {
                    "name": "Geração de Código",
                    "description": "Template para geração de código com base em requisitos",
                    "task_type": "Coding",
                    "structure": {
                        "introduction": "Você gerará código {language} para {task_description}.",
                        "information_gathering": "Se os requisitos não estiverem claros, faça perguntas específicas para entender melhor o que precisa ser implementado.",
                        "process": "Analise os requisitos, planeje a estrutura do código e implemente uma solução eficiente.",
                        "output_format": "Forneça o código completo com comentários explicativos. Use blocos de código formatados apropriadamente.",
                        "additional_context": "Explique as decisões de design, possíveis otimizações e como testar o código."
                    },
                    "example_input": "Crie uma função em Python que verifica se uma string é um palíndromo, ignorando espaços, pontuação e diferenças entre maiúsculas e minúsculas.",
                    "example_output": "```python\ndef is_palindrome(text):\n    \"\"\"\n    Verifica se uma string é um palíndromo, ignorando espaços, pontuação\n    e diferenças entre maiúsculas e minúsculas.\n    \n    Args:\n        text (str): A string a ser verificada\n        \n    Returns:\n        bool: True se a string for um palíndromo, False caso contrário\n    \"\"\"\n    # Importa o módulo para trabalhar com expressões regulares\n    import re\n    \n    # Remove caracteres não alfanuméricos e converte para minúsculas\n    clean_text = re.sub(r'[^a-zA-Z0-9]', '', text).lower()\n    \n    # Verifica se a string limpa é igual à sua versão invertida\n    return clean_text == clean_text[::-1]\n\n# Exemplos de uso\nassert is_palindrome(\"A man, a plan, a canal: Panama\") == True\nassert is_palindrome(\"race a car\") == False\nassert is_palindrome(\"Was it a car or a cat I saw?\") == True\n```\n\nEsta função funciona da seguinte forma:\n\n1. Primeiro, importamos o módulo `re` para usar expressões regulares\n2. Usamos `re.sub()` para remover todos os caracteres não alfanuméricos da string\n3. Convertemos a string resultante para minúsculas com `.lower()`\n4. Verificamos se a string limpa é igual à sua versão invertida (`[::-1]`)\n\nA função lida corretamente com espaços, pontuação e diferenças entre maiúsculas e minúsculas, como demonstrado nos exemplos de teste.\n\nPara testar mais casos, você pode executar o código com diferentes entradas ou criar testes unitários mais abrangentes."
                },
                "content-creation": {
                    "name": "Criação de Conteúdo",
                    "description": "Template para criação de conteúdo criativo ou informativo",
                    "task_type": "Writing",
                    "structure": {
                        "introduction": "Você criará conteúdo {content_type} sobre {topic}.",
                        "information_gathering": "Se precisar de mais detalhes sobre o tema, estilo ou público-alvo, faça perguntas específicas.",
                        "process": "Desenvolva o conteúdo com uma estrutura lógica, começando com uma introdução envolvente, desenvolvendo os pontos principais e concluindo de forma eficaz.",
                        "output_format": "O conteúdo deve ser bem estruturado, com parágrafos claros, títulos quando apropriado, e um estilo adequado ao público-alvo.",
                        "additional_context": "Considere o tom, estilo e nível de formalidade apropriados para o tipo de conteúdo e público."
                    },
                    "example_input": "Escreva um artigo de blog sobre os benefícios da meditação para profissionais ocupados, com foco em técnicas rápidas que podem ser feitas no ambiente de trabalho.",
                    "example_output": "# Meditação para Profissionais Ocupados: Encontrando Calma no Caos Corporativo\n\n## Introdução\n\nNo ritmo acelerado do mundo corporativo moderno, encontrar momentos de tranquilidade parece quase impossível. Reuniões consecutivas, prazos apertados e a constante enxurrada de e-mails criam um ambiente onde o estresse prospera. No entanto, é precisamente neste cenário caótico que a meditação oferece seus benefícios mais poderosos. Este artigo explora como profissionais ocupados podem incorporar práticas meditativas breves mas eficazes em seu dia de trabalho, transformando produtividade e bem-estar sem comprometer agendas já sobrecarregadas.\n\n## Por que meditar no trabalho?\n\nAntes de mergulharmos nas técnicas, vamos entender por que a meditação no ambiente de trabalho vale seu tempo precioso:\n\n- **Redução do estresse em tempo real**: Estudos mostram que mesmo 2-3 minutos de meditação podem reduzir significativamente os hormônios do estresse no corpo\n- **Melhoria do foco**: A prática regular fortalece sua capacidade de manter a atenção em tarefas complexas\n- **Tomada de decisão aprimorada**: Um estado mental mais calmo leva a escolhas mais deliberadas e menos reativas\n- **Criatividade aumentada**: Breves pausas meditativas podem desbloquear soluções inovadoras para problemas persistentes\n- **Melhor relacionamento interpessoal**: A consciência cultivada através da meditação melhora a comunicação e a empatia\n\n## 5 Técnicas de Meditação Rápida para o Ambiente de Trabalho\n\n### 1. Respiração 4-7-8 (2 minutos)\n\nEsta técnica pode ser feita discretamente em sua mesa:\n\n1. Inspire silenciosamente pelo nariz contando até 4\n2. Segure a respiração contando até 7\n3. Expire completamente pela boca contando até 8\n4. Repita 3-4 vezes\n\nIdeal para: Antes de reuniões importantes ou quando sentir ansiedade crescente.\n\n### 2. Escaneamento Corporal Expresso (3 minutos)\n\n1. Sente-se confortavelmente com os pés apoiados no chão\n2. Feche os olhos ou mantenha um olhar suave\n3. Direcione sua atenção metodicamente dos pés à cabeça\n4. Observe tensões e conscientemente relaxe cada área\n\nIdeal para: Após longas sessões de trabalho no computador ou momentos de alta tensão.\n\n[Continua com mais 3 técnicas e seções de conclusão...]\n\n## Conclusão\n\nA meditação não precisa ser uma prática demorada reservada para retiros espirituais. Estas técnicas rápidas demonstram que mesmo os profissionais mais ocupados podem colher os benefícios da atenção plena durante o dia de trabalho. Comece incorporando apenas uma técnica por dia e observe como pequenas pausas para reconexão mental podem transformar sua experiência profissional, aumentando tanto o bem-estar quanto a produtividade.\n\nLembre-se: em um mundo que valoriza a ocupação constante, tirar momentos para acalmar a mente não é apenas benéfico—é estratégico."
                }
            }
            ResourceManager.save_json(TEMPLATES_FILE, templates_data)
        
        # Converter dados em objetos PromptTemplate
        for template_id, template_data in templates_data.items():
            templates[template_id] = PromptTemplate(
                name=template_data.get("name", template_id),
                description=template_data.get("description", ""),
                task_type=template_data.get("task_type", ""),
                structure=template_data.get("structure", {}),
                example_input=template_data.get("example_input", ""),
                example_output=template_data.get("example_output", "")
            )
        
        return templates

# Gerador de prompts
class PromptGenerator:
    def __init__(self):
        self.models = ResourceManager.load_models()
        self.personas = ResourceManager.load_personas()
        self.templates = ResourceManager.load_templates()
        
        # Configurações padrão
        self.selected_model = None
        self.selected_persona = None
        self.selected_template = None
        self.task_description = ""
        self.parameters = {}
        self.user_example = ""
    
    def clear_screen(self):
        """Limpa a tela do terminal"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, text: str):
        """Imprime um cabeçalho formatado"""
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{text.center(80)}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}\n")
    
    def print_section(self, text: str):
        """Imprime um título de seção formatado"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}{text}{Colors.ENDC}")
        print(f"{Colors.BLUE}{'-' * len(text)}{Colors.ENDC}\n")
    
    def print_success(self, text: str):
        """Imprime uma mensagem de sucesso"""
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ {text}{Colors.ENDC}\n")
    
    def print_warning(self, text: str):
        """Imprime uma mensagem de aviso"""
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠ {text}{Colors.ENDC}\n")
    
    def print_error(self, text: str):
        """Imprime uma mensagem de erro"""
        print(f"\n{Colors.RED}{Colors.BOLD}✗ {text}{Colors.ENDC}\n")
    
    def get_input(self, prompt: str, default: str = "") -> str:
        """Obtém entrada do usuário com valor padrão opcional"""
        if default:
            user_input = input(f"{prompt} [{default}]: ")
            return user_input if user_input else default
        else:
            return input(f"{prompt}: ")
    
    def select_from_list(self, items: Dict[str, PromptComponent], prompt: str) -> Optional[str]:
        """Permite ao usuário selecionar um item de uma lista"""
        if not items:
            self.print_error("Nenhum item disponível para seleção.")
            return None
        
        print(f"\n{prompt}\n")
        
        # Exibir itens numerados
        options = list(items.keys())
        for i, item_id in enumerate(options, 1):
            item = items[item_id]
            print(f"{i}. {Colors.BOLD}{item.name}{Colors.ENDC} - {item.description}")
        
        print(f"\n0. {Colors.YELLOW}Voltar{Colors.ENDC}")
        
        # Obter seleção do usuário
        while True:
            try:
                choice = int(input("\nEscolha uma opção (número): "))
                if choice == 0:
                    return None
                elif 1 <= choice <= len(options):
                    return options[choice - 1]
                else:
                    self.print_warning("Opção inválida. Tente novamente.")
            except ValueError:
                self.print_warning("Por favor, digite um número.")
    
    def select_model(self) -> bool:
        """Permite ao usuário selecionar um modelo de IA"""
        model_id = self.select_from_list(self.models, "Selecione o modelo de IA alvo:")
        if model_id:
            self.selected_model = self.models[model_id]
            self.print_success(f"Modelo selecionado: {self.selected_model.name}")
            return True
        return False
    
    def select_persona(self) -> bool:
        """Permite ao usuário selecionar uma persona"""
        persona_id = self.select_from_list(self.personas, "Selecione a persona para o modelo de IA:")
        if persona_id:
            self.selected_persona = self.personas[persona_id]
            self.print_success(f"Persona selecionada: {self.selected_persona.name}")
            return True
        return False
    
    def select_template(self) -> bool:
        """Permite ao usuário selecionar um template de prompt"""
        template_id = self.select_from_list(self.templates, "Selecione o template de prompt:")
        if template_id:
            self.selected_template = self.templates[template_id]
            self.print_success(f"Template selecionado: {self.selected_template.name}")
            return True
        return False
    
    def collect_task_description(self) -> bool:
        """Coleta a descrição da tarefa do usuário"""
        self.print_section("Descrição da Tarefa")
        print("Descreva em detalhes a tarefa que o modelo de IA deve realizar.")
        print("Seja específico sobre o objetivo, contexto e resultado esperado.")
        
        self.task_description = input("\nDescrição da tarefa: ")
        
        if not self.task_description:
            self.print_warning("A descrição da tarefa não pode estar vazia.")
            return False
        
        return True
    
    def collect_parameters(self) -> bool:
        """Coleta parâmetros adicionais para personalização do prompt"""
        self.print_section("Parâmetros Adicionais")
        print("Defina parâmetros adicionais para personalizar o prompt.")
        print("Pressione ENTER sem digitar nada para usar valores padrão.")
        
        # Parâmetros básicos
        self.parameters["tone"] = self.get_input("Tom de comunicação (formal, amigável, técnico, etc.)", 
                                                self.selected_persona.tone if self.selected_persona else "profissional")
        
        self.parameters["detail_level"] = self.get_input("Nível de detalhe (resumido, detalhado, técnico, etc.)", 
                                                        self.selected_persona.detail_level if self.selected_persona else "detalhado")
        
        self.parameters["output_format"] = self.get_input("Formato de saída desejado (texto, markdown, JSON, etc.)", "markdown")
        
        # Parâmetros específicos do template
        if self.selected_template:
            for key in self.selected_template.structure.keys():
                if "{" in self.selected_template.structure[key] and "}" in self.selected_template.structure[key]:
                    # Extrair variáveis entre chaves
                    variables = re.findall(r'\{([^}]+)\}', self.selected_template.structure[key])
                    for var in variables:
                        if var not in self.parameters and var != "topic":  # topic já é coberto pela descrição da tarefa
                            self.parameters[var] = self.get_input(f"Valor para '{var}'")
        
        return True
    
    def collect_example(self) -> bool:
        """Coleta um exemplo opcional do usuário"""
        self.print_section("Exemplo (Opcional)")
        print("Forneça um exemplo de entrada e saída esperada para ajudar o modelo.")
        print("Pressione ENTER sem digitar nada para pular esta etapa.")
        
        example_input = input("\nExemplo de entrada: ")
        if example_input:
            example_output = input("Exemplo de saída esperada: ")
            self.user_example = f"Exemplo de entrada:\n{example_input}\n\nExemplo de saída esperada:\n{example_output}"
        
        return True
    
    def generate_prompt(self) -> Dict[str, str]:
        """Gera o prompt final com base nas seleções e parâmetros"""
        if not (self.selected_model and self.selected_persona and self.selected_template and self.task_description):
            self.print_error("Informações insuficientes para gerar o prompt.")
            return {}
        
        # Preparar o prompt do sistema
        system_prompt = self.selected_persona.system_prompt_template
        
        # Adicionar informações específicas do template
        template_additions = []
        for key, value in self.selected_template.structure.items():
            # Substituir variáveis no template
            formatted_value = value
            for param_key, param_value in self.parameters.items():
                formatted_value = formatted_value.replace(f"{{{param_key}}}", param_value)
            
            # Substituir {topic} pela descrição da tarefa se presente
            formatted_value = formatted_value.replace("{topic}", self.task_description)
            
            template_additions.append(formatted_value)
        
        # Adicionar as adições do template ao prompt do sistema
        if template_additions:
            system_prompt += "\n\n" + "\n\n".join(template_additions)
        
        # Preparar o prompt do usuário
        user_prompt = self.task_description
        
        # Adicionar exemplo se fornecido
        if self.user_example:
            user_prompt += f"\n\n{self.user_example}"
        
        # Criar o prompt final no formato apropriado para o modelo
        prompt = {}
        
        # Garantir que todos os campos do formato do modelo estejam presentes
        for role_key, role_name in self.selected_model.prompt_format.items():
            if role_key == "system":
                prompt[role_name] = system_prompt
            elif role_key == "user":
                prompt[role_name] = user_prompt
            else:
                # Para outros campos (como "assistant"), adicionar um valor vazio
                prompt[role_name] = ""
        
        return prompt
    
    def save_prompt(self, prompt: Dict[str, str]) -> str:
        """Salva o prompt gerado em um arquivo"""
        if not prompt:
            return ""
        
        # Criar nome de arquivo baseado na data/hora e descrição da tarefa
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        task_slug = re.sub(r'[^a-zA-Z0-9]', '_', self.task_description[:30].lower()).strip('_')
        filename = f"{timestamp}_{task_slug}.json"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        # Adicionar metadados
        output_data = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "model": self.selected_model.name if self.selected_model else "",
                "persona": self.selected_persona.name if self.selected_persona else "",
                "template": self.selected_template.name if self.selected_template else "",
                "parameters": self.parameters
            },
            "prompt": prompt
        }
        
        # Salvar arquivo
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
            return filepath
        except Exception as e:
            self.print_error(f"Erro ao salvar o prompt: {e}")
            return ""
    
    def display_prompt(self, prompt: Dict[str, str]):
        """Exibe o prompt gerado"""
        if not prompt:
            return
        
        self.print_section("Prompt Gerado")
        
        for role, content in prompt.items():
            print(f"\n{Colors.CYAN}{Colors.BOLD}{role.upper()}{Colors.ENDC}\n")
            print(content)
    
    def run(self):
        """Executa o fluxo completo de geração de prompt"""
        self.clear_screen()
        self.print_header("Gerador de Prompts para Modelos de IA")
        
        print("Este assistente irá guiá-lo na criação de prompts otimizados para modelos de IA.")
        print("Siga as instruções em cada etapa para gerar um prompt personalizado.")
        
        # Etapa 1: Selecionar modelo
        if not self.select_model():
            self.print_warning("Operação cancelada pelo usuário.")
            return
        
        # Etapa 2: Selecionar persona
        if not self.select_persona():
            self.print_warning("Operação cancelada pelo usuário.")
            return
        
        # Etapa 3: Selecionar template
        if not self.select_template():
            self.print_warning("Operação cancelada pelo usuário.")
            return
        
        # Etapa 4: Coletar descrição da tarefa
        if not self.collect_task_description():
            self.print_warning("Operação cancelada pelo usuário.")
            return
        
        # Etapa 5: Coletar parâmetros adicionais
        if not self.collect_parameters():
            self.print_warning("Operação cancelada pelo usuário.")
            return
        
        # Etapa 6: Coletar exemplo (opcional)
        if not self.collect_example():
            self.print_warning("Operação cancelada pelo usuário.")
            return
        
        # Etapa 7: Gerar prompt
        prompt = self.generate_prompt()
        if not prompt:
            self.print_error("Falha ao gerar o prompt.")
            return
        
        # Etapa 8: Exibir e salvar prompt
        self.display_prompt(prompt)
        
        filepath = self.save_prompt(prompt)
        if filepath:
            self.print_success(f"Prompt salvo com sucesso em: {filepath}")
        
        print("\nPressione ENTER para continuar...")
        input()

# Função principal
def main():
    """Função principal do script"""
    generator = PromptGenerator()
    generator.run()

if __name__ == "__main__":
    main()
