"""
HTML template writer.
"""

from pathlib import Path

from minuta_generator.models import Template


class HTMLWriter:
	"""Writes templates to HTML format."""

	def write(self, template: Template, output_path: Path) -> None:
		"""
		Write template to HTML file.

		Args:
			template: Template to write
			output_path: Path where HTML file should be saved
		"""
		html_content = self._generate_html(template)

		with open(output_path, 'w', encoding='utf-8') as f:
			f.write(html_content)

	def _generate_html(self, template: Template) -> str:
		"""
		Generate HTML content from template.

		Args:
			template: Template to convert

		Returns:
			HTML string
		"""
		# Build sections HTML
		sections_html = []
		for section in template.sections:
			if section.is_variable:
				# Variable sections highlighted
				css_class = 'template-variable'
				title = f'Placeholder: {section.placeholder_name}'
				if section.description:
					title += f' - {section.description}'

				sections_html.append(
					f'<span class="{css_class}" title="{title}" data-placeholder="{section.placeholder_name}">'
					f'{section.content}</span>'
				)
			else:
				# Fixed sections
				sections_html.append(f'<span class="template-fixed">{self._escape_html(section.content)}</span>')

		# Get placeholder info for sidebar
		placeholders_html = []
		seen_placeholders = set()

		for section in template.sections:
			if section.is_variable and section.placeholder_name and section.placeholder_name not in seen_placeholders:
				seen_placeholders.add(section.placeholder_name)
				desc = section.description or section.pattern_type or 'N/A'
				placeholders_html.append(
					f'<li><strong>{section.placeholder_name}</strong>: {desc}</li>'
				)

		placeholders_list = '\n'.join(placeholders_html) if placeholders_html else '<li>Nenhum placeholder</li>'

		# Generate complete HTML
		html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Template: {self._escape_html(template.name)}</title>
	<style>
		body {{
			font-family: 'Times New Roman', serif;
			max-width: 1400px;
			margin: 0 auto;
			padding: 20px;
			background: #f5f5f5;
		}}

		.container {{
			display: grid;
			grid-template-columns: 1fr 300px;
			gap: 20px;
		}}

		.template-content {{
			background: white;
			padding: 40px;
			box-shadow: 0 2px 4px rgba(0,0,0,0.1);
			line-height: 1.6;
			white-space: pre-wrap;
		}}

		.sidebar {{
			background: white;
			padding: 20px;
			box-shadow: 0 2px 4px rgba(0,0,0,0.1);
			position: sticky;
			top: 20px;
			height: fit-content;
		}}

		.template-variable {{
			background: #fff3cd;
			padding: 2px 4px;
			border: 1px dashed #ffc107;
			cursor: help;
			font-weight: bold;
			color: #856404;
		}}

		.template-variable:hover {{
			background: #ffc107;
		}}

		.template-fixed {{
			/* Normal text styling */
		}}

		h1 {{
			color: #333;
			border-bottom: 2px solid #007bff;
			padding-bottom: 10px;
		}}

		h2 {{
			color: #555;
			margin-top: 30px;
		}}

		.sidebar h2 {{
			margin-top: 0;
			font-size: 1.2em;
		}}

		.sidebar ul {{
			list-style: none;
			padding: 0;
		}}

		.sidebar li {{
			padding: 8px 0;
			border-bottom: 1px solid #eee;
		}}

		.sidebar li:last-child {{
			border-bottom: none;
		}}

		.metadata {{
			color: #666;
			font-size: 0.9em;
			margin-top: 20px;
			padding-top: 20px;
			border-top: 1px solid #eee;
		}}

		.legend {{
			margin-top: 20px;
			padding: 10px;
			background: #f8f9fa;
			border-radius: 4px;
			font-size: 0.85em;
		}}

		@media print {{
			body {{
				background: white;
			}}

			.sidebar {{
				display: none;
			}}

			.container {{
				grid-template-columns: 1fr;
			}}

			.template-variable {{
				background: none;
				border: none;
				font-weight: normal;
				color: inherit;
			}}
		}}
	</style>
</head>
<body>
	<h1>Template: {self._escape_html(template.name)}</h1>

	<div class="container">
		<div class="template-content">
			{''.join(sections_html)}

			<div class="metadata">
				<strong>Metadados:</strong><br>
				Documentos originais: {len(template.original_documents)}<br>
				Padrões identificados: {template.metadata.get('num_patterns', 0)}
			</div>
		</div>

		<div class="sidebar">
			<h2>Placeholders</h2>
			<ul>
				{placeholders_list}
			</ul>

			<div class="legend">
				<strong>Legenda:</strong><br>
				<span class="template-variable">Texto destacado</span> = Campo variável<br>
				Texto normal = Conteúdo fixo
			</div>
		</div>
	</div>
</body>
</html>"""

		return html

	@staticmethod
	def _escape_html(text: str) -> str:
		"""Escape HTML special characters."""
		return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
