from app.core.llm_provider import OpenAIProvider, GeminiProvider

def get_llm_provider(provider_name: str, settings):
    providers = {
        "openai": (OpenAIProvider, settings.OPENAI_API_KEY),
        "gemini": (GeminiProvider, settings.GEMINI_API_KEY),
    }
    if provider_name not in providers:
        raise ValueError(f"Unsupported LLM provider: {provider_name}")
    provider_class, api_key = providers[provider_name]
    return provider_class(api_key) 