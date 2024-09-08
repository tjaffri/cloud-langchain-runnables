from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langgraph.graph import StateGraph

from cloud_langchain_runnables.common import LLM, SimpleGraphState

prompt = ChatPromptTemplate.from_messages(
    [
        HumanMessagePromptTemplate.from_template(
            """Your task is to read a candidate resume and return a unique summary of their overall experience.
Here is the resume to summarize: 

{resume_text}"""
        )
    ]
)

# Create runnable
resume_summary_runnable = prompt | LLM


# Create graph
def resume_summary_node(state: SimpleGraphState) -> SimpleGraphState:
    input = str(state.get("input"))
    return {
        "output": resume_summary_runnable.invoke(input).content,
    }


workflow = StateGraph(SimpleGraphState)
workflow.add_node("resume_summary", resume_summary_node)
workflow.set_entry_point("resume_summary")
workflow.set_finish_point("resume_summary")
resume_summary_graph = workflow.compile()

