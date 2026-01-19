"""
Minuta Generator - Sistema de automação para criação de templates de minutas jurídicas usando IA.

Este sistema analisa documentos jurídicos existentes e gera templates reutilizáveis
com placeholders para partes variáveis, facilitando a criação de novas minutas.
"""

__version__ = '0.1.0'

from minuta_generator.models import (
	AnalysisResult,
	Document,
	DocumentFormat,
	LLMConfig,
	LLMProvider,
	PatternMatch,
	Template,
	TemplateFormat,
	TemplateSection,
)

__all__ = [
	'Document',
	'DocumentFormat',
	'Template',
	'TemplateFormat',
	'TemplateSection',
	'PatternMatch',
	'AnalysisResult',
	'LLMConfig',
	'LLMProvider',
]
