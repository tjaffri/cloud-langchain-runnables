from langchain_core.runnables import RunnableLambda
from langgraph.graph import Graph

def add_one(x: int) -> int:
    """Add one to an integer."""
    return x + 1

# Create simple runnable
add_one_runnable = RunnableLambda(add_one)

# Wrap in a simple graph
workflow = Graph()
workflow.add_node("add_one", add_one)
workflow.set_entry_point("add_one")
add_one_graph = workflow.compile()
