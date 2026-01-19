"""
Pydantic models for the legal template generator.
"""

from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class DocumentFormat(str, Enum):
	"""Supported document formats."""

	PDF = 'pdf'
	DOC = 'doc'
	DOCX = 'docx'
	HTML = 'html'


class TemplateFormat(str, Enum):
	"""Supported template output formats."""

	HTML = 'html'
	DOCX = 'docx'


class LLMProvider(str, Enum):
	"""Supported LLM providers."""

	GOOGLE = 'google'  # Google Gemini
	LOCAL = 'local'  # Local models via Ollama or compatible API


class Document(BaseModel):
	"""Represents a legal document."""

	model_config = ConfigDict(extra='forbid')

	path: Path
	format: DocumentFormat
	content: str
	metadata: dict[str, Any] = Field(default_factory=dict)


class PatternMatch(BaseModel):
	"""Represents a pattern found in documents."""

	model_config = ConfigDict(extra='forbid')

	text: str
	pattern_type: str  # e.g., "heading", "signature", "date", "case_number"
	confidence: float = Field(ge=0.0, le=1.0)
	examples: list[str] = Field(default_factory=list)
	suggested_placeholder: str  # e.g., "{{CASE_NUMBER}}", "{{AUTHOR_NAME}}"


class TemplateSection(BaseModel):
	"""Represents a section of a template."""

	model_config = ConfigDict(extra='forbid')

	content: str
	is_variable: bool = False  # Whether this section should be replaced
	placeholder_name: str | None = None
	pattern_type: str | None = None
	description: str | None = None


class Template(BaseModel):
	"""Represents a generated template."""

	model_config = ConfigDict(extra='forbid')

	name: str
	sections: list[TemplateSection]
	metadata: dict[str, Any] = Field(default_factory=dict)
	original_documents: list[Path] = Field(default_factory=list)


class LLMConfig(BaseModel):
	"""Configuration for LLM provider."""

	model_config = ConfigDict(extra='forbid')

	provider: LLMProvider
	api_key: str | None = None
	model_name: str | None = None
	base_url: str | None = None  # For local models
	temperature: float = Field(default=0.3, ge=0.0, le=2.0)
	max_tokens: int = Field(default=4096, gt=0)


class AnalysisResult(BaseModel):
	"""Result of pattern analysis."""

	model_config = ConfigDict(extra='forbid')

	patterns: list[PatternMatch]
	common_structure: str  # Description of common document structure
	suggestions: list[str]  # Suggested improvements or observations
