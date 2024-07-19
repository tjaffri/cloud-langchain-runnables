from langchain_core.runnables import RunnableLambda


def add_one(x: int) -> int:
    """Add one to an integer."""
    return x + 1


add_one_runnable = RunnableLambda(add_one)
