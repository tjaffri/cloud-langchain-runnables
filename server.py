import os
from fastapi import Depends, FastAPI, Header, HTTPException
from langchain_core.runnables import RunnableLambda
from typing_extensions import Annotated

from langserve import add_routes


async def verify_token(x_token: Annotated[str, Header()]) -> None:
    """Verify the token is valid."""
    # Replace this with your actual authentication logic
    if x_token != os.getenv("SECRET"):
        raise HTTPException(status_code=400, detail="X-Token header invalid")


app = FastAPI(
    title="LangChain Server",
    version="1.0",
    dependencies=[Depends(verify_token)],
)


def add_one(x: int) -> int:
    """Add one to an integer."""
    return x + 1


chain = RunnableLambda(add_one)


add_routes(app, chain, path="/add_one")

if __name__ == "__main__":
    import uvicorn

    port = 8000
    port_env = os.getenv("PORT")
    if port_env:
        port = int(port_env)

    uvicorn.run(app, host="localhost", port=port)
