#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de Validação do Gerador de Prompts
-----------------------------------------

Este script testa o funcionamento do gerador de prompts,
verificando se ele consegue carregar recursos e gerar
prompts válidos para diferentes modelos e casos de uso.

Autor: Manus AI
Data: Junho 2025
"""

import os
import sys
import json
import unittest
from pathlib import Path

# Adicionar o diretório de scripts ao path
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.append(parent_dir + "/scripts")

# Importar o módulo do gerador de prompts
try:
    from prompt_generator import ResourceManager, AIModel, Persona, PromptTemplate, PromptGenerator
except ImportError:
    print("Erro ao importar o módulo do gerador de prompts. Verifique se o arquivo está no diretório correto.")
    sys.exit(1)

class TestPromptGenerator(unittest.TestCase):
    """Testes para o gerador de prompts"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.resources_dir = os.path.join(parent_dir, "resources")
        self.output_dir = os.path.join(parent_dir, "output")
        
        # Garantir que os diretórios existam
        os.makedirs(self.resources_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Caminhos para os arquivos de recursos
        self.personas_file = os.path.join(self.resources_dir, "personas.json")
        self.templates_file = os.path.join(self.resources_dir, "templates.json")
        self.models_file = os.path.join(self.resources_dir, "models.json")
        
        # Inicializar o gerador de prompts
        self.generator = PromptGenerator()
    
    def test_resource_files_exist(self):
        """Verifica se os arquivos de recursos existem"""
        self.assertTrue(os.path.exists(self.personas_file), f"Arquivo de personas não encontrado: {self.personas_file}")
        self.assertTrue(os.path.exists(self.templates_file), f"Arquivo de templates não encontrado: {self.templates_file}")
        self.assertTrue(os.path.exists(self.models_file), f"Arquivo de modelos não encontrado: {self.models_file}")
    
    def test_load_models(self):
        """Testa o carregamento de modelos"""
        models = ResourceManager.load_models()
        self.assertIsNotNone(models, "Falha ao carregar modelos")
        self.assertGreater(len(models), 0, "Nenhum modelo carregado")
        
        # Verificar se os modelos Claude estão presentes
        self.assertIn("claude-opus-4", models, "Modelo Claude Opus 4 não encontrado")
        self.assertIn("claude-sonnet-4", models, "Modelo Claude Sonnet 4 não encontrado")
        self.assertIn("claude-3-7-sonnet", models, "Modelo Claude Sonnet 3.7 não encontrado")
    
    def test_load_personas(self):
        """Testa o carregamento de personas"""
        personas = ResourceManager.load_personas()
        self.assertIsNotNone(personas, "Falha ao carregar personas")
        self.assertGreater(len(personas), 0, "Nenhuma persona carregada")
        
        # Verificar se algumas personas básicas estão presentes
        self.assertIn("excel-expert", personas, "Persona Excel Expert não encontrada")
        self.assertIn("code-developer", personas, "Persona Code Developer não encontrada")
    
    def test_load_templates(self):
        """Testa o carregamento de templates"""
        templates = ResourceManager.load_templates()
        self.assertIsNotNone(templates, "Falha ao carregar templates")
        self.assertGreater(len(templates), 0, "Nenhum template carregado")
        
        # Verificar se alguns templates básicos estão presentes
        self.assertIn("qa-template", templates, "Template QA não encontrado")
        self.assertIn("code-generation", templates, "Template Code Generation não encontrado")
    
    def test_generate_prompt(self):
        """Testa a geração de um prompt completo"""
        # Configurar o gerador com valores de teste
        self.generator.selected_model = AIModel(
            name="Claude Opus 4",
            description="Modelo mais capaz e inteligente da Anthropic",
            provider="Anthropic",
            context_window=200000,
            max_output=32000,
            features={"extended_thinking": True, "vision": True, "multilingual": True},
            prompt_format={"system": "system", "user": "user", "assistant": "assistant"},
            training_cutoff="2025-03"
        )
        
        self.generator.selected_persona = Persona(
            name="Excel Formula Expert",
            description="Especialista em criar fórmulas do Excel",
            expertise=["Excel", "Fórmulas", "Análise de dados"],
            tone="Técnico mas acessível",
            detail_level="Detalhado com explicações passo a passo",
            approach="Analítico e explicativo",
            system_prompt_template="Como um Excel Formula Expert, sua tarefa é fornecer fórmulas avançadas do Excel."
        )
        
        self.generator.selected_template = PromptTemplate(
            name="Pergunta e Resposta",
            description="Template para perguntas e respostas diretas",
            task_type="QA",
            structure={
                "introduction": "Você responderá perguntas sobre {topic}.",
                "information_gathering": "Se a pergunta for ambígua, peça esclarecimentos.",
                "process": "Analise a pergunta cuidadosamente.",
                "output_format": "Sua resposta deve ser clara e concisa.",
                "additional_context": "Forneça contexto adicional quando relevante."
            },
            example_input="Exemplo de entrada",
            example_output="Exemplo de saída"
        )
        
        self.generator.task_description = "Criar fórmulas do Excel para análise de vendas"
        self.generator.parameters = {
            "tone": "técnico",
            "detail_level": "detalhado",
            "output_format": "markdown"
        }
        
        # Gerar o prompt
        prompt = self.generator.generate_prompt()
        
        # Verificar se o prompt foi gerado corretamente
        self.assertIsNotNone(prompt, "Falha ao gerar prompt")
        self.assertIn("system", prompt, "Prompt não contém campo 'system'")
        self.assertIn("user", prompt, "Prompt não contém campo 'user'")
        
        # Verificar se o conteúdo do prompt inclui elementos esperados
        system_prompt = prompt["system"]
        self.assertIn("Excel Formula Expert", system_prompt, "Persona não incluída no prompt")
        self.assertIn("análise de vendas", system_prompt, "Descrição da tarefa não incluída no prompt")
    
    def test_prompt_json_structure(self):
        """Testa se o prompt gerado segue uma estrutura JSON válida e completa"""
        # Configurar o gerador com valores de teste (simplificado do teste anterior)
        self.generator.selected_model = next(iter(ResourceManager.load_models().values()))
        self.generator.selected_persona = next(iter(ResourceManager.load_personas().values()))
        self.generator.selected_template = next(iter(ResourceManager.load_templates().values()))
        self.generator.task_description = "Tarefa de teste para validação JSON"
        self.generator.parameters = {"tone": "neutro", "detail_level": "médio", "output_format": "texto"}
        
        # Gerar o prompt
        prompt = self.generator.generate_prompt()
        
        # Verificar se o prompt pode ser serializado como JSON válido
        try:
            prompt_json = json.dumps(prompt, ensure_ascii=False)
            parsed_prompt = json.loads(prompt_json)
            
            # Verificar se a estrutura foi preservada
            self.assertEqual(prompt.keys(), parsed_prompt.keys(), "Estrutura JSON alterada durante serialização")
            
        except Exception as e:
            self.fail(f"Falha ao serializar/deserializar o prompt como JSON: {e}")
    
    def test_multi_model_compatibility(self):
        """Testa a compatibilidade do prompt com múltiplos modelos"""
        # Lista de modelos para testar
        model_ids = ["claude-opus-4", "claude-sonnet-4", "claude-3-7-sonnet", "gpt-4", "gemini-pro"]
        models = ResourceManager.load_models()
        
        # Configurações básicas para o teste
        self.generator.selected_persona = next(iter(ResourceManager.load_personas().values()))
        self.generator.selected_template = next(iter(ResourceManager.load_templates().values()))
        self.generator.task_description = "Tarefa de teste para compatibilidade multi-modelo"
        self.generator.parameters = {"tone": "neutro", "detail_level": "médio", "output_format": "texto"}
        
        # Testar com cada modelo
        for model_id in model_ids:
            if model_id in models:
                self.generator.selected_model = models[model_id]
                prompt = self.generator.generate_prompt()
                
                # Verificar se o prompt foi gerado corretamente para este modelo
                self.assertIsNotNone(prompt, f"Falha ao gerar prompt para modelo {model_id}")
                
                # Verificar se o formato do prompt está correto para o modelo específico
                expected_format = self.generator.selected_model.prompt_format
                for key in expected_format.values():
                    self.assertIn(key, prompt, f"Formato incorreto para modelo {model_id}: falta campo '{key}'")

def run_tests():
    """Executa os testes de validação"""
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

if __name__ == "__main__":
    print("Iniciando validação do gerador de prompts...\n")
    run_tests()
