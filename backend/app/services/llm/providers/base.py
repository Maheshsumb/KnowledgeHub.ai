from abc import ABC, abstractmethod
from typing import Iterator, AsyncIterator


class BaseLLMProvider(ABC):

    @abstractmethod
    def generate(
        self,
        prompt: str,
    ) -> str:
        pass

    @abstractmethod
    async def stream(
        self,
        prompt: str,
    ) -> AsyncIterator[str]:
        pass