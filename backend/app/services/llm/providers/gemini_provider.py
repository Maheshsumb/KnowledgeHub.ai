from typing import Iterator, AsyncIterator

from langchain_google_genai import ChatGoogleGenerativeAI

from app.services.llm.providers.base import BaseLLMProvider
from app.core.config import settings


class GeminiProvider(BaseLLMProvider):

    def __init__(self):

        self.model = ChatGoogleGenerativeAI(
            model="gemini-3.5-flash-lite",
            temperature=0,
            api_key=settings.GOOGLE_API_KEY,
        )

    @property
    def model_name(self) -> str:
        return "gemini-2.5-flash"

    def generate(
        self,
        prompt: str,
    ) -> str:

        response = self.model.invoke(prompt)
        content = response.content

        if isinstance(content, list):
            # Extract text from blocks
            text_parts = []
            for block in content:
                if isinstance(block, str):
                    text_parts.append(block)
                elif isinstance(block, dict) and "text" in block:
                    text_parts.append(block["text"])
            return "".join(text_parts)

        return str(content)

    async def stream(
        self,
        prompt: str,
    ) -> AsyncIterator[str]:

        async for chunk in self.model.astream(prompt):
            content = chunk.content
            if not content:
                continue
                
            if isinstance(content, list):
                for block in content:
                    if isinstance(block, str):
                        yield block
                    elif isinstance(block, dict) and "text" in block:
                        yield block["text"]
            else:
                yield str(content)
