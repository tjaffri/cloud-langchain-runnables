from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.runnables import RunnableLambda
from langgraph.graph import StateGraph, MessagesState


def add_one(x: int) -> int:
    """Add one to an integer."""
    return x + 2


# Create runnable
add_one_runnable = RunnableLambda(add_one)


# Create graph
def add_one_node(state: MessagesState):
    messages = state.get("messages")
    assert len(messages) > 0
    last_message = messages[-1]
    assert isinstance(last_message, HumanMessage)

    input = int(last_message.content)
    output = add_one(input)
    return {"messages": AIMessage(str(output))}  # replace the list of messages


workflow = StateGraph(MessagesState)
workflow.add_node("add_one", add_one_node)
workflow.set_entry_point("add_one")
workflow.set_finish_point("add_one")
add_one_graph = workflow.compile()
