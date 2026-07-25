from typing import Iterator, AsyncIterator

from app.services.llm.providers.base import BaseLLMProvider


class LLMService:

    def __init__(
        self,
        provider: BaseLLMProvider,
    ):
        self.provider = provider

    @property
    def model_name(self) -> str:
        return self.provider.model_name

    def generate(
        self,
        prompt: str,
    ) -> str:

        return self.provider.generate(prompt)

    async def stream(
        self,
        prompt: str,
    ) -> AsyncIterator[str]:

        async for chunk in self.provider.stream(prompt):
            yield chunk