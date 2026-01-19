"""
Google Gemini LLM provider.
"""

import json

import google.generativeai as genai

from minuta_generator.llm.base import BaseLLM
from minuta_generator.models import LLMConfig


class GoogleLLM(BaseLLM):
	"""Google Gemini LLM provider."""

	def __init__(self, config: LLMConfig):
		super().__init__(config)
		self._validate_config()

		if not config.api_key:
			raise ValueError('Google API key is required')

		genai.configure(api_key=config.api_key)

		# Use default model if not specified
		model_name = config.model_name or 'gemini-2.0-flash-exp'

		self.model = genai.GenerativeModel(
			model_name=model_name,
			generation_config=genai.GenerationConfig(
				temperature=config.temperature, max_output_tokens=config.max_tokens
			),
		)

	async def generate(self, prompt: str, system_prompt: str | None = None) -> str:
		"""
		Generate text using Google Gemini.

		Args:
			prompt: User prompt
			system_prompt: Optional system prompt

		Returns:
			Generated text response
		"""
		# Combine system and user prompts if system prompt provided
		full_prompt = prompt
		if system_prompt:
			full_prompt = f'{system_prompt}\n\n{prompt}'

		response = await self.model.generate_content_async(full_prompt)

		if not response.text:
			raise ValueError('Empty response from Gemini API')

		return response.text

	async def generate_json(self, prompt: str, system_prompt: str | None = None) -> dict:
		"""
		Generate structured JSON output using Google Gemini.

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
