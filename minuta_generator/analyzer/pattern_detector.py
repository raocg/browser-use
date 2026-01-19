"""
Pattern detection in legal documents using LLM.
"""

from minuta_generator.llm.base import BaseLLM
from minuta_generator.models import AnalysisResult, Document, PatternMatch


class PatternDetector:
	"""Detects patterns in legal documents using LLM analysis."""

	def __init__(self, llm: BaseLLM):
		self.llm = llm

	async def analyze_documents(self, documents: list[Document]) -> AnalysisResult:
		"""
		Analyze multiple documents to find common patterns.

		Args:
			documents: List of documents to analyze

		Returns:
			AnalysisResult with identified patterns
		"""
		if not documents:
			raise ValueError('At least one document is required for analysis')

		# Prepare document contents for analysis
		doc_contents = []
		for idx, doc in enumerate(documents, start=1):
			doc_contents.append(f'=== DOCUMENTO {idx} ({doc.path.name}) ===\n{doc.content}\n')

		combined_content = '\n\n'.join(doc_contents)

		# Create analysis prompt
		system_prompt = """Você é um especialista em análise de documentos jurídicos.
Sua tarefa é identificar padrões comuns em minutas jurídicas para criar templates reutilizáveis.

Identifique:
1. Seções que aparecem em todos ou na maioria dos documentos
2. Partes variáveis que mudam entre documentos (nomes, datas, números de processo, etc.)
3. Estrutura comum dos documentos
4. Sugestões de placeholders para partes variáveis

Seja preciso e identifique padrões reais, não suposições."""

		prompt = f"""Analise os seguintes documentos jurídicos e identifique padrões comuns:

{combined_content}

Retorne um JSON com a seguinte estrutura:
{{
	"patterns": [
		{{
			"text": "texto do padrão encontrado",
			"pattern_type": "tipo (heading, signature, date, case_number, party_name, etc.)",
			"confidence": 0.95,
			"examples": ["exemplo 1", "exemplo 2"],
			"suggested_placeholder": "{{{{NOME_DO_PLACEHOLDER}}}}"
		}}
	],
	"common_structure": "Descrição da estrutura comum dos documentos",
	"suggestions": ["Sugestão 1", "Sugestão 2"]
}}

Certifique-se de identificar:
- Cabeçalhos e títulos comuns
- Campos de identificação (números de processo, partes, etc.)
- Datas e prazos
- Assinaturas e qualificações
- Seções de fundamentação jurídica
- Pedidos e requerimentos
"""

		# Get LLM analysis
		response_json = await self.llm.generate_json(prompt, system_prompt)

		# Parse patterns
		patterns = [PatternMatch(**pattern_data) for pattern_data in response_json.get('patterns', [])]

		return AnalysisResult(
			patterns=patterns,
			common_structure=response_json.get('common_structure', ''),
			suggestions=response_json.get('suggestions', []),
		)

	async def analyze_single_document(self, document: Document) -> AnalysisResult:
		"""
		Analyze a single document to identify its structure.

		Args:
			document: Document to analyze

		Returns:
			AnalysisResult with identified structure and variable parts
		"""
		system_prompt = """Você é um especialista em análise de documentos jurídicos.
Identifique a estrutura deste documento e as partes que provavelmente são variáveis
(que mudariam em outros documentos similares)."""

		prompt = f"""Analise este documento jurídico:

{document.content}

Identifique:
1. A estrutura do documento (seções principais)
2. Partes que provavelmente são variáveis e devem ser substituídas por placeholders
3. Tipo de documento (petição inicial, contestação, recurso, etc.)

Retorne JSON com:
{{
	"patterns": [
		{{
			"text": "texto identificado",
			"pattern_type": "tipo",
			"confidence": 0.9,
			"examples": ["exemplo"],
			"suggested_placeholder": "{{{{PLACEHOLDER}}}}"
		}}
	],
	"common_structure": "descrição da estrutura",
	"suggestions": ["sugestões de melhoria"]
}}
"""

		response_json = await self.llm.generate_json(prompt, system_prompt)

		patterns = [PatternMatch(**pattern_data) for pattern_data in response_json.get('patterns', [])]

		return AnalysisResult(
			patterns=patterns,
			common_structure=response_json.get('common_structure', ''),
			suggestions=response_json.get('suggestions', []),
		)
