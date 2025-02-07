from langchain_openai import ChatOpenAI

LLM = ChatOpenAI(model="o3-mini", max_completion_tokens=1024, timeout=60 * 2, max_retries=2)

result = LLM.invoke("Hello, world!")
print(result)
