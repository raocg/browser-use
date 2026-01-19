"""
Local LLM provider (via OpenAI-compatible API like Ollama).
"""

import json

from openai import AsyncOpenAI

from minuta_generator.llm.base import BaseLLM
from minuta_generator.models import LLMConfig


class LocalLLM(BaseLLM):
	"""Local LLM provider using OpenAI-compatible API."""

	def __init__(self, config: LLMConfig):
		super().__init__(config)
		self._validate_config()

		# Default to Ollama's default endpoint if not specified
		base_url = config.base_url or 'http://localhost:11434/v1'

		# Default model for local setup
		model_name = config.model_name or 'llama3.2'

		self.client = AsyncOpenAI(
			api_key=config.api_key or 'not-needed',  # Ollama doesn't require API key
			base_url=base_url,
		)

		self.model_name = model_name

	async def generate(self, prompt: str, system_prompt: str | None = None) -> str:
		"""
		Generate text using local LLM.

		Args:
			prompt: User prompt
			system_prompt: Optional system prompt

		Returns:
			Generated text response
		"""
		messages = []

		if system_prompt:
			messages.append({'role': 'system', 'content': system_prompt})

		messages.append({'role': 'user', 'content': prompt})

		response = await self.client.chat.completions.create(
			model=self.model_name,
			messages=messages,
			temperature=self.config.temperature,
			max_tokens=self.config.max_tokens,
		)

		if not response.choices or not response.choices[0].message.content:
			raise ValueError('Empty response from local LLM')

		return response.choices[0].message.content

	async def generate_json(self, prompt: str, system_prompt: str | None = None) -> dict:
		"""
		Generate structured JSON output using local LLM.

		Args:
			prompt: User prompt
			system_prompt: Optional system prompt

		Returns:
			Parsed JSON response
		"""
		# Add JSON instruction to prompt
		json_prompt = f'{prompt}\n\nResponda APENAS com JSON válido, sem texto adicional antes ou depois.'

		response_text = await self.generate(json_prompt, system_prompt)

		# Try to extract JSON from response
		try:
			# Try direct parsing first
			return json.loads(response_text)
		except json.JSONDecodeError:
			# Try to find JSON in markdown code blocks
			if '```json' in response_text:
				json_start = response_text.find('```json') + 7
				json_end = response_text.find('```', json_start)
				json_text = response_text[json_start:json_end].strip()
				return json.loads(json_text)
			elif '```' in response_text:
				json_start = response_text.find('```') + 3
				json_end = response_text.find('```', json_start)
				json_text = response_text[json_start:json_end].strip()
				return json.loads(json_text)
			else:
				raise ValueError(f'Failed to parse JSON from response: {response_text[:200]}...')
