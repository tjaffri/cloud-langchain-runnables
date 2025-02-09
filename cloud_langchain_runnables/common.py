from typing import Any, TypedDict
from langchain_openai import ChatOpenAI

class SimpleGraphState(TypedDict):
    input: Any
    output: Any

# LLM = ChatOpenAI(
#     model="gpt-4o", temperature=0, max_tokens=1024, timeout=60 * 2, max_retries=2
# )

LLM = ChatOpenAI(model="o3-mini", reasoning_effort="low", max_completion_tokens=1024, timeout=60 * 2, max_retries=2)