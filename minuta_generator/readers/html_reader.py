"""
HTML document reader.
"""

from pathlib import Path

from bs4 import BeautifulSoup

from minuta_generator.models import Document, DocumentFormat
from minuta_generator.readers.base import DocumentReader


class HTMLReader(DocumentReader):
	"""Reader for HTML documents."""

	def supported_format(self) -> DocumentFormat:
		return DocumentFormat.HTML

	def read(self, file_path: Path) -> Document:
		"""
		Read an HTML document.

		Args:
			file_path: Path to the HTML file

		Returns:
			Document object with extracted text content
		"""
		self.validate_file(file_path)

		with open(file_path, 'r', encoding='utf-8') as f:
			html_content = f.read()

		soup = BeautifulSoup(html_content, 'lxml')

		# Remove script and style elements
		for script in soup(['script', 'style', 'meta', 'link']):
			script.decompose()

		# Extract text
		text = soup.get_text(separator='\n', strip=True)

		# Extract metadata from HTML meta tags and title
		metadata = {
			'title': soup.title.string if soup.title else '',
			'has_forms': bool(soup.find_all('form')),
			'has_tables': bool(soup.find_all('table')),
		}

		# Try to extract common meta tags
		meta_tags = {}
		for meta in soup.find_all('meta'):
			name = meta.get('name', meta.get('property', ''))
			content = meta.get('content', '')
			if name and content:
				meta_tags[name] = content

		if meta_tags:
			metadata['meta_tags'] = meta_tags

		return Document(path=file_path, format=DocumentFormat.HTML, content=text, metadata=metadata)
