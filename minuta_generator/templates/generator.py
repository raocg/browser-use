"""
Template generation from analyzed documents.
"""

from minuta_generator.llm.base import BaseLLM
from minuta_generator.models import AnalysisResult, Document, Template, TemplateSection
from minuta_generator.templates.placeholder import PlaceholderManager


class TemplateGenerator:
	"""Generates templates from document analysis."""

	def __init__(self, llm: BaseLLM):
		self.llm = llm
		self.placeholder_manager = PlaceholderManager()

	async def generate_from_analysis(
		self, documents: list[Document], analysis: AnalysisResult, template_name: str
	) -> Template:
		"""
		Generate a template from document analysis.

		Args:
			documents: Original documents that were analyzed
			analysis: Analysis results with identified patterns
			template_name: Name for the generated template

		Returns:
			Generated Template object
		"""
		# Use the first document as base, or combine if multiple
		if len(documents) == 1:
			base_content = documents[0].content
		else:
			# Ask LLM to create a merged template from multiple documents
			base_content = await self._merge_documents(documents, analysis)

		# Create template sections by replacing patterns with placeholders
		sections = await self._create_sections(base_content, analysis)

		return Template(
			name=template_name,
			sections=sections,
			metadata={'num_patterns': len(analysis.patterns), 'common_structure': analysis.common_structure},
			original_documents=[doc.path for doc in documents],
		)

	async def _merge_documents(self, documents: list[Document], analysis: AnalysisResult) -> str:
		"""
		Merge multiple documents into a single base template.

		Args:
			documents: Documents to merge
			analysis: Analysis with common patterns

		Returns:
			Merged document content
		"""
		doc_contents = '\n\n---\n\n'.join([f'DOCUMENTO {i+1}:\n{doc.content}' for i, doc in enumerate(documents)])

		system_prompt = """Você é um especialista em criar templates de documentos jurídicos.
Sua tarefa é criar um documento base que combine os melhores elementos de vários documentos similares."""

		prompt = f"""Com base nos seguintes documentos e na análise de padrões, crie um documento base único
que servirá como template:

DOCUMENTOS:
{doc_contents}

ESTRUTURA COMUM IDENTIFICADA:
{analysis.common_structure}

PADRÕES IDENTIFICADOS:
{len(analysis.patterns)} padrões foram encontrados

Crie um documento base mantendo:
1. A estrutura comum a todos os documentos
2. O texto que aparece de forma similar em todos
3. Exemplos das partes variáveis (que serão substituídas depois)

Retorne apenas o texto do documento base, sem comentários adicionais.
"""

		return await self.llm.generate(prompt, system_prompt)

	async def _create_sections(self, base_content: str, analysis: AnalysisResult) -> list[TemplateSection]:
		"""
		Create template sections from base content and analysis.

		Args:
			base_content: Base document content
			analysis: Analysis with identified patterns

		Returns:
			List of TemplateSection objects
		"""
		# Sort patterns by confidence (highest first)
		sorted_patterns = sorted(analysis.patterns, key=lambda p: p.confidence, reverse=True)

		# Ask LLM to segment the document and mark variable sections
		system_prompt = """Você é um especialista em criar templates estruturados de documentos jurídicos.
Divida o documento em seções, identificando quais partes devem ser variáveis (substituíveis)."""

		patterns_description = '\n'.join(
			[f'- {p.pattern_type}: {p.suggested_placeholder} (confiança: {p.confidence})' for p in sorted_patterns]
		)

		prompt = f"""Divida este documento em seções e identifique quais partes devem ser placeholders:

DOCUMENTO:
{base_content}

PADRÕES IDENTIFICADOS:
{patterns_description}

Retorne JSON com:
{{
	"sections": [
		{{
			"content": "texto da seção",
			"is_variable": false,
			"placeholder_name": null,
			"pattern_type": null,
			"description": "descrição da seção"
		}},
		{{
			"content": "texto variável exemplo",
			"is_variable": true,
			"placeholder_name": "NUMERO_PROCESSO",
			"pattern_type": "case_number",
			"description": "número do processo"
		}}
	]
}}

Regras:
- Seções fixas (is_variable=false) contêm texto que aparece sempre igual
- Seções variáveis (is_variable=true) são partes que mudam entre documentos
- Use os placeholders sugeridos nos padrões identificados
- Mantenha a ordem do documento original
"""

		response_json = await self.llm.generate_json(prompt, system_prompt)

		sections = []
		for section_data in response_json.get('sections', []):
			# Replace content with placeholder if it's a variable section
			content = section_data['content']
			if section_data.get('is_variable') and section_data.get('placeholder_name'):
				placeholder = self.placeholder_manager.create_placeholder(section_data['placeholder_name'])
				content = placeholder

			sections.append(
				TemplateSection(
					content=content,
					is_variable=section_data.get('is_variable', False),
					placeholder_name=section_data.get('placeholder_name'),
					pattern_type=section_data.get('pattern_type'),
					description=section_data.get('description'),
				)
			)

		return sections

	def template_to_text(self, template: Template) -> str:
		"""
		Convert a Template object to plain text.

		Args:
			template: Template to convert

		Returns:
			Text representation of the template
		"""
		return '\n'.join([section.content for section in template.sections])

	def get_required_placeholders(self, template: Template) -> dict[str, str]:
		"""
		Get all required placeholders from a template.

		Args:
			template: Template to analyze

		Returns:
			Dictionary mapping placeholder names to descriptions
		"""
		placeholders = {}
		for section in template.sections:
			if section.is_variable and section.placeholder_name:
				placeholders[section.placeholder_name] = section.description or section.pattern_type or 'N/A'

		return placeholders
