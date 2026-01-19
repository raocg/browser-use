"""
Document readers for various formats.
"""

from minuta_generator.readers.base import DocumentReader
from minuta_generator.readers.docx_reader import DOCXReader
from minuta_generator.readers.html_reader import HTMLReader
from minuta_generator.readers.pdf_reader import PDFReader

__all__ = ['DocumentReader', 'PDFReader', 'DOCXReader', 'HTMLReader']
