"""
Exemplo de uso programático do Minuta Generator.

Este script demonstra como usar a biblioteca programaticamente
ao invés de usar a interface de linha de comando.
"""

import asyncio
from pathlib import Path

from minuta_generator.analyzer import PatternDetector
from minuta_generator.llm import GoogleLLM, LocalLLM
from minuta_generator.models import LLMConfig, LLMProvider
from minuta_generator.readers import DOCXReader, HTMLReader, PDFReader
from minuta_generator.templates import TemplateGenerator
from minuta_generator.writers import DOCXWriter, HTMLWriter


async def example_single_document_analysis():
	"""Exemplo: Analisar um único documento."""
	print('=== Exemplo 1: Análise de Documento Único ===\n')

	# Configurar LLM (Google Gemini)
	llm_config = LLMConfig(
		provider=LLMProvider.GOOGLE,
		api_key='your-api-key-here',  # Ou use variável de ambiente
		model_name='gemini-2.0-flash-exp',
		temperature=0.3,
	)

	llm = GoogleLLM(llm_config)

	# Ler documento
	pdf_reader = PDFReader()
	document = pdf_reader.read(Path('exemplo.pdf'))

	print(f'Documento lido: {document.path.name}')
	print(f'Tamanho: {len(document.content)} caracteres\n')

	# Analisar padrões
	detector = PatternDetector(llm)
	analysis = await detector.analyze_single_document(document)

	print(f'Padrões identificados: {len(analysis.patterns)}')
	print(f'\nEstrutura comum:\n{analysis.common_structure}\n')

	# Mostrar padrões
	for pattern in analysis.patterns[:5]:  # Primeiros 5
		print(f'- {pattern.pattern_type}: {pattern.suggested_placeholder} ({pattern.confidence:.0%})')


async def example_multiple_documents_template():
	"""Exemplo: Gerar template a partir de múltiplos documentos."""
	print('\n=== Exemplo 2: Geração de Template de Múltiplos Documentos ===\n')

	# Configurar LLM (modelo local via Ollama)
	llm_config = LLMConfig(
		provider=LLMProvider.LOCAL,
		base_url='http://localhost:11434/v1',
		model_name='llama3.2',
		temperature=0.3,
	)

	llm = LocalLLM(llm_config)

	# Ler múltiplos documentos
	documents = []

	pdf_reader = PDFReader()
	docx_reader = DOCXReader()

	# Exemplo: 2 PDFs e 1 DOCX
	doc1 = pdf_reader.read(Path('petição1.pdf'))
	doc2 = pdf_reader.read(Path('petição2.pdf'))
	doc3 = docx_reader.read(Path('petição3.docx'))

	documents = [doc1, doc2, doc3]

	print(f'Documentos lidos: {len(documents)}')

	# Analisar padrões comuns
	detector = PatternDetector(llm)
	analysis = await detector.analyze_documents(documents)

	print(f'Padrões comuns identificados: {len(analysis.patterns)}\n')

	# Gerar template
	generator = TemplateGenerator(llm)
	template = await generator.generate_from_analysis(documents, analysis, 'Petição Inicial Padrão')

	print(f'Template gerado: {template.name}')
	print(f'Seções: {len(template.sections)}')

	# Obter placeholders necessários
	placeholders = generator.get_required_placeholders(template)
	print(f'\nPlaceholders necessários: {len(placeholders)}')
	for name, description in placeholders.items():
		print(f'  - {name}: {description}')

	# Salvar em HTML
	html_writer = HTMLWriter()
	html_writer.write(template, Path('template_gerado.html'))
	print('\n✓ Template salvo em: template_gerado.html')

	# Salvar em DOCX
	docx_writer = DOCXWriter()
	docx_writer.write(template, Path('template_gerado.docx'))
	print('✓ Template salvo em: template_gerado.docx')


async def example_custom_analysis():
	"""Exemplo: Análise customizada com controle fino."""
	print('\n=== Exemplo 3: Análise Customizada ===\n')

	# Usar diferentes temperaturas para diferentes propósitos
	# Temperatura baixa (0.1) = mais conservador e preciso
	# Temperatura alta (0.7) = mais criativo

	llm_config_conservative = LLMConfig(
		provider=LLMProvider.GOOGLE,
		api_key='your-api-key-here',
		temperature=0.1,  # Muito conservador
		max_tokens=8192,
	)

	llm = GoogleLLM(llm_config_conservative)

	# Ler documento HTML
	html_reader = HTMLReader()
	document = html_reader.read(Path('decisão.html'))

	# Analisar
	detector = PatternDetector(llm)
	analysis = await detector.analyze_single_document(document)

	print(f'Análise com temperatura conservadora (0.1):')
	print(f'Padrões: {len(analysis.patterns)}')
	print(f'Sugestões: {len(analysis.suggestions)}')

	# Mostrar sugestões
	if analysis.suggestions:
		print('\nSugestões do LLM:')
		for suggestion in analysis.suggestions:
			print(f'  • {suggestion}')


async def example_template_manipulation():
	"""Exemplo: Manipular template programaticamente."""
	print('\n=== Exemplo 4: Manipulação de Template ===\n')

	# Assumindo que já temos um template gerado
	# Este exemplo mostra como trabalhar com ele

	from minuta_generator.models import Template, TemplateSection
	from minuta_generator.templates import PlaceholderManager

	# Criar template manualmente (normalmente viria de análise)
	sections = [
		TemplateSection(content='EXCELENTÍSSIMO SENHOR DOUTOR JUIZ DE DIREITO DA ', is_variable=False),
		TemplateSection(
			content='{{VARA}}',
			is_variable=True,
			placeholder_name='VARA',
			pattern_type='court',
			description='Vara competente',
		),
		TemplateSection(content=' DE ', is_variable=False),
		TemplateSection(
			content='{{CIDADE}}',
			is_variable=True,
			placeholder_name='CIDADE',
			pattern_type='city',
			description='Cidade da vara',
		),
		TemplateSection(content='\n\n', is_variable=False),
		TemplateSection(
			content='{{NOME_PARTE}}',
			is_variable=True,
			placeholder_name='NOME_PARTE',
			pattern_type='party_name',
			description='Nome da parte autora',
		),
	]

	template = Template(name='Exemplo Manual', sections=sections)

	# Converter para texto
	from minuta_generator.templates import TemplateGenerator

	llm_config = LLMConfig(provider=LLMProvider.LOCAL)  # Dummy config
	llm = LocalLLM(llm_config)
	generator = TemplateGenerator(llm)

	template_text = generator.template_to_text(template)
	print('Template como texto:')
	print(template_text)

	# Preencher placeholders
	pm = PlaceholderManager()
	filled_text = pm.fill_placeholders(
		template_text, {'VARA': '1ª Vara Cível', 'CIDADE': 'São Paulo', 'NOME_PARTE': 'João da Silva'}
	)

	print('\nTemplate preenchido:')
	print(filled_text)

	# Extrair placeholders de um texto
	placeholders = pm.extract_placeholders(template_text)
	print(f'\nPlaceholders encontrados: {placeholders}')


async def main():
	"""Executa todos os exemplos."""
	print('MINUTA GENERATOR - Exemplos de Uso Programático')
	print('=' * 60)
	print()

	# Descomente os exemplos que deseja executar:

	# await example_single_document_analysis()
	# await example_multiple_documents_template()
	# await example_custom_analysis()
	await example_template_manipulation()

	print('\n' + '=' * 60)
	print('Exemplos concluídos!')


if __name__ == '__main__':
	asyncio.run(main())
