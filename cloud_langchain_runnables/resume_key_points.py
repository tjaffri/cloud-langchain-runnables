from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langgraph.graph import StateGraph

from cloud_langchain_runnables.common import LLM, SimpleGraphState

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


# Create runnable
resume_key_points_runnable = prompt | LLM


# Create graph
def resume_key_points_node(state: SimpleGraphState) -> SimpleGraphState:
    input = str(state.get("input"))
    return {
        "output": resume_key_points_runnable.invoke(input).content,
    }


workflow = StateGraph(SimpleGraphState)
workflow.add_node("resume_key_points", resume_key_points_node)
workflow.set_entry_point("resume_key_points")
workflow.set_finish_point("resume_key_points")
resume_key_points_graph = workflow.compile()
