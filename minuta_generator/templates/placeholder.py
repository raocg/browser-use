"""
Placeholder management for templates.
"""

import re
from typing import Any


class PlaceholderManager:
	"""Manages template placeholders."""

	PLACEHOLDER_PATTERN = r'\{\{([A-Z_]+)\}\}'

	@staticmethod
	def create_placeholder(name: str) -> str:
		"""
		Create a placeholder string.

		Args:
			name: Placeholder name (will be converted to uppercase)

		Returns:
			Formatted placeholder string like {{NAME}}
		"""
		clean_name = name.upper().replace(' ', '_')
		return f'{{{{{clean_name}}}}}'

	@staticmethod
	def extract_placeholders(text: str) -> list[str]:
		"""
		Extract all placeholders from text.

		Args:
			text: Text containing placeholders

		Returns:
			List of placeholder names (without braces)
		"""
		matches = re.findall(PlaceholderManager.PLACEHOLDER_PATTERN, text)
		return list(set(matches))  # Remove duplicates

	@staticmethod
	def fill_placeholders(template: str, values: dict[str, Any]) -> str:
		"""
		Fill template placeholders with values.

		Args:
			template: Template string with placeholders
			values: Dictionary mapping placeholder names to values

		Returns:
			Template with placeholders replaced

		Raises:
			ValueError: If required placeholders are missing
		"""
		required_placeholders = PlaceholderManager.extract_placeholders(template)
		missing = set(required_placeholders) - set(values.keys())

		if missing:
			raise ValueError(f'Missing values for placeholders: {missing}')

		result = template
		for placeholder, value in values.items():
			pattern = f'{{{{{placeholder}}}}}'
			result = result.replace(pattern, str(value))

		return result

	@staticmethod
	def validate_placeholder_name(name: str) -> bool:
		"""
		Validate that a placeholder name follows conventions.

		Args:
			name: Placeholder name to validate

		Returns:
			True if valid, False otherwise
		"""
		# Should be uppercase letters, numbers, and underscores only
		return bool(re.match(r'^[A-Z_][A-Z0-9_]*$', name))

	@staticmethod
	def suggest_placeholder_name(text: str, pattern_type: str) -> str:
		"""
		Suggest a placeholder name based on text and pattern type.

		Args:
			text: Sample text for this placeholder
			pattern_type: Type of pattern (e.g., 'date', 'name', 'case_number')

		Returns:
			Suggested placeholder name
		"""
		# Map pattern types to standard placeholder names
		type_mapping = {
			'date': 'DATA',
			'case_number': 'NUMERO_PROCESSO',
			'party_name': 'NOME_PARTE',
			'lawyer_name': 'NOME_ADVOGADO',
			'signature': 'ASSINATURA',
			'judge_name': 'NOME_JUIZ',
			'court': 'VARA',
			'city': 'CIDADE',
			'state': 'ESTADO',
			'heading': 'TITULO',
			'subject': 'ASSUNTO',
		}

		# Try to get from mapping first
		base_name = type_mapping.get(pattern_type, pattern_type.upper())

		# Clean up the name
		clean_name = re.sub(r'[^A-Z0-9_]', '_', base_name.upper())
		clean_name = re.sub(r'_+', '_', clean_name)  # Remove duplicate underscores
		clean_name = clean_name.strip('_')

		return clean_name
