"""
Basic tests for minuta_generator components.
"""

import pytest
from pathlib import Path

from minuta_generator.models import (
	Document,
	DocumentFormat,
	LLMConfig,
	LLMProvider,
	PatternMatch,
	Template,
	TemplateSection,
)
from minuta_generator.templates.placeholder import PlaceholderManager


def test_document_model():
	"""Test Document model creation and validation."""
	doc = Document(
		path=Path('test.pdf'), format=DocumentFormat.PDF, content='Test content', metadata={'test': 'value'}
	)

	assert doc.path == Path('test.pdf')
	assert doc.format == DocumentFormat.PDF
	assert doc.content == 'Test content'
	assert doc.metadata['test'] == 'value'


def test_pattern_match_model():
	"""Test PatternMatch model with validation."""
	pattern = PatternMatch(
		text='Processo nº 12345',
		pattern_type='case_number',
		confidence=0.95,
		examples=['12345', '67890'],
		suggested_placeholder='{{NUMERO_PROCESSO}}',
	)

	assert pattern.confidence == 0.95
	assert len(pattern.examples) == 2

	# Test confidence validation
	with pytest.raises(Exception):  # Pydantic validation error
		PatternMatch(
			text='test',
			pattern_type='test',
			confidence=1.5,  # Invalid: > 1.0
			suggested_placeholder='{{TEST}}',
		)


def test_template_section_model():
	"""Test TemplateSection model."""
	section = TemplateSection(
		content='{{NOME_PARTE}}',
		is_variable=True,
		placeholder_name='NOME_PARTE',
		pattern_type='party_name',
		description='Nome da parte autora',
	)

	assert section.is_variable is True
	assert section.placeholder_name == 'NOME_PARTE'


def test_template_model():
	"""Test Template model with sections."""
	sections = [
		TemplateSection(content='Texto fixo', is_variable=False),
		TemplateSection(content='{{VAR}}', is_variable=True, placeholder_name='VAR'),
	]

	template = Template(name='Test Template', sections=sections)

	assert template.name == 'Test Template'
	assert len(template.sections) == 2
	assert template.sections[0].is_variable is False
	assert template.sections[1].is_variable is True


def test_llm_config_model():
	"""Test LLMConfig model."""
	config = LLMConfig(provider=LLMProvider.GOOGLE, api_key='test-key', model_name='gemini-2.0-flash-exp')

	assert config.provider == LLMProvider.GOOGLE
	assert config.api_key == 'test-key'
	assert config.temperature == 0.3  # Default value


def test_placeholder_manager_create():
	"""Test placeholder creation."""
	pm = PlaceholderManager()

	placeholder = pm.create_placeholder('numero_processo')
	assert placeholder == '{{NUMERO_PROCESSO}}'

	placeholder = pm.create_placeholder('nome parte')
	assert placeholder == '{{NOME_PARTE}}'


def test_placeholder_manager_extract():
	"""Test placeholder extraction from text."""
	pm = PlaceholderManager()

	text = 'Nome: {{NOME}} no processo {{NUMERO_PROCESSO}} em {{DATA}}'
	placeholders = pm.extract_placeholders(text)

	assert len(placeholders) == 3
	assert 'NOME' in placeholders
	assert 'NUMERO_PROCESSO' in placeholders
	assert 'DATA' in placeholders


def test_placeholder_manager_fill():
	"""Test placeholder filling."""
	pm = PlaceholderManager()

	template = 'Processo {{NUMERO}} da parte {{NOME}}'
	values = {'NUMERO': '12345', 'NOME': 'João Silva'}

	result = pm.fill_placeholders(template, values)
	assert result == 'Processo 12345 da parte João Silva'


def test_placeholder_manager_fill_missing():
	"""Test placeholder filling with missing values."""
	pm = PlaceholderManager()

	template = 'Processo {{NUMERO}} da parte {{NOME}}'
	values = {'NUMERO': '12345'}  # Missing 'NOME'

	with pytest.raises(ValueError, match='Missing values'):
		pm.fill_placeholders(template, values)


def test_placeholder_validation():
	"""Test placeholder name validation."""
	pm = PlaceholderManager()

	assert pm.validate_placeholder_name('NOME_PARTE') is True
	assert pm.validate_placeholder_name('NUMERO123') is True
	assert pm.validate_placeholder_name('_TESTE') is True

	assert pm.validate_placeholder_name('nome-parte') is False  # Lowercase and hyphen
	assert pm.validate_placeholder_name('123NUMERO') is False  # Starts with number
	assert pm.validate_placeholder_name('NOME PARTE') is False  # Space


def test_placeholder_suggest_name():
	"""Test placeholder name suggestion."""
	pm = PlaceholderManager()

	name = pm.suggest_placeholder_name('12345-67.2024', 'case_number')
	assert name == 'NUMERO_PROCESSO'

	name = pm.suggest_placeholder_name('João da Silva', 'party_name')
	assert name == 'NOME_PARTE'

	name = pm.suggest_placeholder_name('01/01/2024', 'date')
	assert name == 'DATA'
