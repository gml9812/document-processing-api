from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Dict
from .llm_provider import LLMProvider, LLMMessage, LLMConfig

T = TypeVar('T')

class DocumentProcessor(ABC, Generic[T]):
    """
    Abstract base class for document processors.
    Generic type T represents the specific document schema (e.g., BusinessLicense, Invoice).
    """
    def __init__(self, llm_provider: LLMProvider, model_name: str = "gpt-4"):
        self.llm = llm_provider
        self.config = LLMConfig(
            temperature=0,
            model_name=model_name
        )

    async def _generate_response(self, messages: List[LLMMessage]) -> str:
        return await self.llm.generate(messages, self.config)

    async def _generate_structured_response(self, messages: List[LLMMessage], json_schema: Dict) -> Dict:
        return await self.llm.generate_with_json_output(messages, json_schema, self.config)

    @abstractmethod
    async def process_document(self, text: str, keywords: List[str], language: str) -> T:
        """
        Process a document and extract structured information.

        Args:
            text (str): The raw text extracted from the document
            keywords (List[str]): List of keywords to focus on during extraction
            language (str): The language of the document

        Returns:
            T: The processed document data in the appropriate schema
        """
        pass 