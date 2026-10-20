from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

def call_llm(prompt: str) -> str:
    model_name = os.getenv("DEEPSEEK_MODEL", "deepseek-v4-pro")
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}]
    )
    # print(f"[LLM REQUEST] model={model_name}")
    # print(f"[LLM RESPONSE] model={getattr(response, 'model', 'unknown')}")
    return response.choices[0].message.content

