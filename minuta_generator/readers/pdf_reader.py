"""
PDF document reader.
"""

from pathlib import Path

from pypdf import PdfReader

from minuta_generator.models import Document, DocumentFormat
from minuta_generator.readers.base import DocumentReader


class PDFReader(DocumentReader):
	"""Reader for PDF documents."""

	def supported_format(self) -> DocumentFormat:
		return DocumentFormat.PDF

	def read(self, file_path: Path) -> Document:
		"""
		Read a PDF document.

		Args:
			file_path: Path to the PDF file

		Returns:
			Document object with extracted text content
		"""
		self.validate_file(file_path)

		pdf_reader = PdfReader(file_path)

		# Extract text from all pages
		text_content = []
		for page_num, page in enumerate(pdf_reader.pages, start=1):
			page_text = page.extract_text()
			if page_text:
				text_content.append(page_text)

		# Extract metadata
		metadata = {
			'num_pages': len(pdf_reader.pages),
			'has_metadata': bool(pdf_reader.metadata),
		}

		if pdf_reader.metadata:
			metadata.update(
				{
					'title': pdf_reader.metadata.get('/Title', ''),
					'author': pdf_reader.metadata.get('/Author', ''),
					'subject': pdf_reader.metadata.get('/Subject', ''),
					'creator': pdf_reader.metadata.get('/Creator', ''),
				}
			)

		return Document(
			path=file_path, format=DocumentFormat.PDF, content='\n\n'.join(text_content), metadata=metadata
		)
