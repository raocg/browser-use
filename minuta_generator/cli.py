"""
CLI interface for minuta-generator.
"""

import asyncio
from pathlib import Path

import click
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from minuta_generator.analyzer import PatternDetector
from minuta_generator.llm import GoogleLLM, LocalLLM
from minuta_generator.models import DocumentFormat, LLMConfig, LLMProvider, TemplateFormat
from minuta_generator.readers import DOCXReader, HTMLReader, PDFReader
from minuta_generator.templates import TemplateGenerator
from minuta_generator.writers import DOCXWriter, HTMLWriter

# Load environment variables
load_dotenv()

console = Console()


def get_reader(file_path: Path):
	"""Get appropriate reader for file format."""
	suffix = file_path.suffix.lower()

	if suffix == '.pdf':
		return PDFReader()
	elif suffix == '.docx':
		return DOCXReader()
	elif suffix in ['.html', '.htm']:
		return HTMLReader()
	else:
		raise ValueError(f'Unsupported file format: {suffix}')


def get_writer(output_format: str):
	"""Get appropriate writer for output format."""
	if output_format == 'html':
		return HTMLWriter()
	elif output_format == 'docx':
		return DOCXWriter()
	else:
		raise ValueError(f'Unsupported output format: {output_format}')


@click.group()
@click.version_option(version='0.1.0')
def cli():
	"""
	Minuta Generator - Sistema de automação para criação de templates de minutas jurídicas.

	Analisa documentos jurídicos e gera templates reutilizáveis com placeholders.
	"""
	pass


@cli.command()
@click.argument('input_files', nargs=-1, type=click.Path(exists=True), required=True)
@click.option('--output', '-o', type=click.Path(), required=True, help='Caminho do arquivo de saída')
@click.option(
	'--format',
	'-f',
	type=click.Choice(['html', 'docx']),
	default='html',
	help='Formato de saída (html ou docx)',
)
@click.option('--name', '-n', help='Nome do template (padrão: nome do primeiro arquivo)')
@click.option('--provider', type=click.Choice(['google', 'local']), default='google', help='Provedor de LLM')
@click.option('--api-key', envvar='GOOGLE_API_KEY', help='API key do Google (ou use GOOGLE_API_KEY env var)')
@click.option('--model', help='Nome do modelo LLM (padrão: gemini-2.0-flash-exp para Google, llama3.2 para local)')
@click.option('--base-url', help='URL base para modelo local (padrão: http://localhost:11434/v1)')
@click.option('--temperature', type=float, default=0.3, help='Temperatura do LLM (padrão: 0.3)')
def generate(input_files, output, format, name, provider, api_key, model, base_url, temperature):
	"""
	Gera um template a partir de documentos jurídicos.

	INPUT_FILES: Um ou mais arquivos de entrada (.pdf, .docx, .html)

	Exemplos:

	  # Analisar um único arquivo com Google Gemini
	  minuta-generator generate documento.pdf -o template.html

	  # Analisar múltiplos arquivos e gerar DOCX
	  minuta-generator generate doc1.pdf doc2.docx doc3.html -o template.docx -f docx

	  # Usar modelo local
	  minuta-generator generate documento.pdf -o template.html --provider local
	"""
	asyncio.run(_generate_async(input_files, output, format, name, provider, api_key, model, base_url, temperature))


async def _generate_async(input_files, output, format, name, provider, api_key, model, base_url, temperature):
	"""Async implementation of generate command."""
	try:
		# Validate provider-specific requirements
		if provider == 'google' and not api_key:
			console.print(
				'[red]Erro: Google API key é necessária. '
				'Use --api-key ou defina GOOGLE_API_KEY como variável de ambiente.[/red]'
			)
			return

		# Show header
		console.print(Panel.fit('[bold blue]Minuta Generator[/bold blue]', border_style='blue'))

		# Configure LLM
		llm_config = LLMConfig(
			provider=LLMProvider(provider),
			api_key=api_key,
			model_name=model,
			base_url=base_url,
			temperature=temperature,
		)

		if provider == 'google':
			llm = GoogleLLM(llm_config)
		else:
			llm = LocalLLM(llm_config)

		# Read documents
		documents = []
		with Progress(SpinnerColumn(), TextColumn('[progress.description]{task.description}'), console=console) as progress:
			task = progress.add_task('Lendo documentos...', total=len(input_files))

			for file_path_str in input_files:
				file_path = Path(file_path_str)
				reader = get_reader(file_path)

				doc = reader.read(file_path)
				documents.append(doc)

				console.print(f'✓ Lido: [cyan]{file_path.name}[/cyan] ({len(doc.content)} caracteres)')
				progress.advance(task)

		# Analyze documents
		console.print('\n[yellow]Analisando documentos com LLM...[/yellow]')
		detector = PatternDetector(llm)

		with console.status('[bold yellow]Identificando padrões...'):
			analysis = await detector.analyze_documents(documents)

		# Show analysis results
		console.print(f'\n[green]✓ Análise concluída![/green]')
		console.print(f'  Padrões identificados: {len(analysis.patterns)}')

		# Create table of patterns
		if analysis.patterns:
			table = Table(title='Padrões Identificados')
			table.add_column('Tipo', style='cyan')
			table.add_column('Placeholder', style='yellow')
			table.add_column('Confiança', style='green')

			for pattern in analysis.patterns[:10]:  # Show first 10
				table.add_row(pattern.pattern_type, pattern.suggested_placeholder, f'{pattern.confidence:.2%}')

			console.print(table)

		# Generate template
		template_name = name or Path(input_files[0]).stem
		console.print(f'\n[yellow]Gerando template: {template_name}...[/yellow]')

		generator = TemplateGenerator(llm)

		with console.status('[bold yellow]Criando template...'):
			template = await generator.generate_from_analysis(documents, analysis, template_name)

		console.print(f'[green]✓ Template gerado com {len(template.sections)} seções![/green]')

		# Write output
		output_path = Path(output)
		writer = get_writer(format)

		console.print(f'\n[yellow]Salvando template em: {output_path}...[/yellow]')
		writer.write(template, output_path)

		console.print(f'\n[bold green]✓ Template salvo com sucesso![/bold green]')
		console.print(f'  Arquivo: [cyan]{output_path.absolute()}[/cyan]')

		# Show placeholders
		placeholders = generator.get_required_placeholders(template)
		if placeholders:
			console.print(f'\n[bold]Placeholders no template:[/bold]')
			for placeholder, description in placeholders.items():
				console.print(f'  • {placeholder}: {description}')

	except Exception as e:
		console.print(f'[bold red]Erro:[/bold red] {str(e)}')
		raise


@cli.command()
@click.argument('input_file', type=click.Path(exists=True), required=True)
@click.option('--provider', type=click.Choice(['google', 'local']), default='google', help='Provedor de LLM')
@click.option('--api-key', envvar='GOOGLE_API_KEY', help='API key do Google')
@click.option('--model', help='Nome do modelo LLM')
@click.option('--base-url', help='URL base para modelo local')
def analyze(input_file, provider, api_key, model, base_url):
	"""
	Analisa um documento e mostra os padrões identificados.

	INPUT_FILE: Arquivo a ser analisado (.pdf, .docx, .html)
	"""
	asyncio.run(_analyze_async(input_file, provider, api_key, model, base_url))


async def _analyze_async(input_file, provider, api_key, model, base_url):
	"""Async implementation of analyze command."""
	try:
		if provider == 'google' and not api_key:
			console.print('[red]Erro: Google API key é necessária.[/red]')
			return

		console.print(Panel.fit('[bold blue]Análise de Documento[/bold blue]', border_style='blue'))

		# Configure LLM
		llm_config = LLMConfig(provider=LLMProvider(provider), api_key=api_key, model_name=model, base_url=base_url)

		if provider == 'google':
			llm = GoogleLLM(llm_config)
		else:
			llm = LocalLLM(llm_config)

		# Read document
		file_path = Path(input_file)
		reader = get_reader(file_path)
		doc = reader.read(file_path)

		console.print(f'✓ Documento: [cyan]{file_path.name}[/cyan]')
		console.print(f'  Tamanho: {len(doc.content)} caracteres\n')

		# Analyze
		detector = PatternDetector(llm)

		with console.status('[bold yellow]Analisando...'):
			analysis = await detector.analyze_single_document(doc)

		# Show results
		console.print(f'[green]✓ Análise concluída![/green]\n')

		# Structure
		console.print(Panel(analysis.common_structure, title='[bold]Estrutura Identificada[/bold]', border_style='blue'))

		# Patterns
		if analysis.patterns:
			table = Table(title=f'\nPadrões Identificados ({len(analysis.patterns)})')
			table.add_column('Tipo', style='cyan', width=20)
			table.add_column('Placeholder', style='yellow', width=25)
			table.add_column('Confiança', style='green', width=10)
			table.add_column('Exemplo', style='white')

			for pattern in analysis.patterns:
				example = pattern.examples[0] if pattern.examples else pattern.text[:50] + '...'
				table.add_row(pattern.pattern_type, pattern.suggested_placeholder, f'{pattern.confidence:.0%}', example)

			console.print(table)

		# Suggestions
		if analysis.suggestions:
			console.print('\n[bold]Sugestões:[/bold]')
			for suggestion in analysis.suggestions:
				console.print(f'  • {suggestion}')

	except Exception as e:
		console.print(f'[bold red]Erro:[/bold red] {str(e)}')
		raise


def main():
	"""Entry point for CLI."""
	cli()


if __name__ == '__main__':
	main()
