import asyncio
from openai import AsyncOpenAI
from app.config import get_settings
from app.utils.prompts import SYSTEM_PROMPT

class AIService:
    def __init__(self):
        st = get_settings()
        self.model = st.openai_model
        self.timeout = st.ai_request_timeout
        self.client = AsyncOpenAI(api_key=st.openai_api_key)

    async def _call(self, user_input: str) -> str:
        r = await asyncio.wait_for(
            self.client.responses.create(model=self.model, instructions=SYSTEM_PROMPT, input=user_input),
            timeout=self.timeout,
        )
        text = (r.output_text or "").strip()
        if not text:
            raise RuntimeError("AI empty response")
        return text

    async def generate(self, data: dict) -> str:
        user = "\n".join(f"{k}: {v}" for k, v in data.items() if v)
        return await self._call(user)

    async def revise(self, old: str, instruction: str) -> str:
        return await self._call(f"OLDINGI XAT:\n{old}\n\nTAHRIR KO‘RSATMASI:\n{instruction}\n\nYangi fakt qo‘shma.")
