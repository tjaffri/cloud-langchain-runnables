from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import Graph

prompt = ChatPromptTemplate.from_messages(
    [
        HumanMessagePromptTemplate.from_template(
            """Your task is to review candidate resumes and extract key data points.
You are to find the First Name, Surname, Email Address, Current Company Name, and Current Position in that order.
The response should be in CSV format without headers and without any surrounding ticks or quotes.
Please note that First Name and Surname are to be distinct columns.
Here is the resume to extract from:

{resume_text}"""
        )
    ]
)

llm = ChatOpenAI(
    model="gpt-4o", temperature=0, max_tokens=1024, timeout=60 * 2, max_retries=2
)

resume_key_points_runnable = prompt | llm

def resume_key_points(x: dict) -> str:
    return resume_key_points_runnable.invoke(x)


# Wrap in a simple graph
workflow = Graph()
workflow.add_node("resume_key_points", resume_key_points)
workflow.set_entry_point("resume_key_points")
resume_key_points_graph = workflow.compile()
