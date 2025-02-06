from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
import json

class LLMMessage(BaseModel):
    role: str
    content: str

class LLMConfig(BaseModel):
    temperature: float = 0
    max_tokens: Optional[int] = None
    model_name: str

class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, messages: List[LLMMessage], config: LLMConfig) -> str:
        """Generate response from LLM"""
        pass

    @abstractmethod
    async def generate_with_json_output(self, messages: List[LLMMessage], json_schema: Dict, config: LLMConfig) -> Dict:
        """Generate response with JSON output"""
        pass

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str):
        from openai import AsyncOpenAI
        self.client = AsyncOpenAI(api_key=api_key)
    
    async def generate(self, messages: List[LLMMessage], config: LLMConfig) -> str:
        response = await self.client.chat.completions.create(
            model=config.model_name,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            messages=[{"role": m.role, "content": m.content} for m in messages]
        )
        return response.choices[0].message.content

    async def generate_with_json_output(self, messages: List[LLMMessage], json_schema: Dict, config: LLMConfig) -> Dict:
        messages.append(LLMMessage(
            role="system",
            content=f"You must respond with valid JSON matching this schema: {json_schema}"
        ))
        response = await self.generate(messages, config)
        return json.loads(response)

class GeminiProvider(LLMProvider):
    def __init__(self, api_key: str):
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        self.genai = genai
    
    async def generate(self, messages: List[LLMMessage], config: LLMConfig) -> str:
        model = self.genai.GenerativeModel(config.model_name)
        chat = model.start_chat()
        full_prompt = "\n".join(f"{msg.role.upper()}: {msg.content}" for msg in messages)
        response = await chat.send_message_async(full_prompt)
        return response.text.strip()

    async def generate_with_json_output(self, messages: List[LLMMessage], json_schema: Dict, config: LLMConfig) -> Dict:
        # Insert the JSON directive at the beginning so that it stays in context.
        json_instruction = LLMMessage(
            role="system",
            content=f"You must respond with valid JSON matching this schema: {json_schema}"
        )
        messages.insert(0, json_instruction)
        response_text = await self.generate(messages, config)
        if not response_text:
            raise ValueError("Empty response received from Gemini.")
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON response from Gemini: {response_text}") 