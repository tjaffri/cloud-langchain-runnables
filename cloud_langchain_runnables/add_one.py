from langchain_core.runnables import RunnableLambda
from langgraph.graph import StateGraph

from cloud_langchain_runnables.common import SimpleGraphState


def add_one(x: int) -> int:
    """Add one to an integer."""
    return x + 1


# Create runnable
add_one_runnable = RunnableLambda(add_one)


# Create graph
def add_one_node(state: SimpleGraphState) -> SimpleGraphState:
    input_val = state.get("input")
    if input_val is None:
        raise ValueError("Input value is required")
    input_num = int(str(input_val))
    return SimpleGraphState(input=str(input_num), output=str(add_one(input_num)))


workflow = StateGraph(SimpleGraphState)
workflow.add_node("add_one", add_one_node)
workflow.set_entry_point("add_one")
workflow.set_finish_point("add_one")
add_one_graph = workflow.compile()
