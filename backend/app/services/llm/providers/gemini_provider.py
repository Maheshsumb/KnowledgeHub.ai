from langchain_google_genai import ChatGoogleGenerativeAI

from app.services.llm.providers.base import BaseLLMProvider
from app.core.config import settings


class GeminiProvider(BaseLLMProvider):

    def __init__(self):

        self.model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
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

        return response.content