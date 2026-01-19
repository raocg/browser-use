"""
Base LLM provider interface.
"""

from abc import ABC, abstractmethod

from minuta_generator.models import LLMConfig


class BaseLLM(ABC):
	"""Base class for LLM providers."""

	def __init__(self, config: LLMConfig):
		self.config = config

	@abstractmethod
	async def generate(self, prompt: str, system_prompt: str | None = None) -> str:
		"""
		Generate text using the LLM.

		Args:
			prompt: User prompt
			system_prompt: Optional system prompt

		Returns:
			Generated text response
		"""
		pass

	@abstractmethod
	async def generate_json(self, prompt: str, system_prompt: str | None = None) -> dict:
		"""
		Generate structured JSON output using the LLM.

		Args:
			prompt: User prompt
			system_prompt: Optional system prompt

		Returns:
			Parsed JSON response
		"""
		pass

	def _validate_config(self) -> None:
		"""Validate that required configuration is present."""
		if self.config.provider.value not in ['google', 'local']:
			raise ValueError(f'Unsupported provider: {self.config.provider}')
