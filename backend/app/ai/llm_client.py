import os
from typing import Dict

from openai import OpenAI


class LLMClient:

    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url=os.getenv("OPENROUTER_BASE_URL"),
        )
        self.model = os.getenv("OPENROUTER_MODEL", "openai/gpt-oss-120b:free")

    def generate(self, prompt: Dict[str, str]) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": prompt["system"]},
                {"role": "user", "content": prompt["user"]},
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content