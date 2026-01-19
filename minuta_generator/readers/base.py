"""
Base document reader interface.
"""

from abc import ABC, abstractmethod
from pathlib import Path

from minuta_generator.models import Document, DocumentFormat


class DocumentReader(ABC):
	"""Base class for document readers."""

	@abstractmethod
	def read(self, file_path: Path) -> Document:
		"""
		Read a document from the given file path.

		Args:
			file_path: Path to the document file

		Returns:
			Document object with extracted content
		"""
		pass

	@abstractmethod
	def supported_format(self) -> DocumentFormat:
		"""
		Return the document format this reader supports.

		Returns:
			DocumentFormat enum value
		"""
		pass

	def validate_file(self, file_path: Path) -> None:
		"""
		Validate that the file exists and has the correct extension.

		Args:
			file_path: Path to validate

		Raises:
			FileNotFoundError: If file doesn't exist
			ValueError: If file extension doesn't match supported format
		"""
		if not file_path.exists():
			raise FileNotFoundError(f'File not found: {file_path}')

		expected_ext = f'.{self.supported_format().value}'
		if file_path.suffix.lower() != expected_ext:
			raise ValueError(f'Expected {expected_ext} file, got {file_path.suffix}')
