from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import Graph

prompt = ChatPromptTemplate.from_messages(
    [
        HumanMessagePromptTemplate.from_template(
            """Your task is to read a candidate resume and return a unique summary of their overall experience.
Here is the resume to summarize: 

{resume_text}"""
        )
    ]
)

llm = ChatOpenAI(
    model="gpt-4o", temperature=0, max_tokens=1024, timeout=60 * 2, max_retries=2
)

resume_summary_runnable = prompt | llm


def resume_summary(x: str) -> str:
    return resume_summary_runnable.invoke(
        {
            "resume_text": x,
        }
    )


# Wrap in a simple graph
workflow = Graph()
workflow.add_node("resume_summary", resume_summary)
workflow.set_entry_point("resume_summary")
resume_summary_graph = workflow.compile()
