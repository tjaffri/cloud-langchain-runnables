import os
from fastapi import Depends, FastAPI, Header, HTTPException
from typing_extensions import Annotated

from langserve import add_routes
from runnables.add_one import add_one_runnable


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


add_routes(app, add_one_runnable, path="/add_one")

if __name__ == "__main__":
    import uvicorn

    port = 8000
    port_env = os.getenv("PORT")
    if port_env:
        port = int(port_env)

    uvicorn.run(app, host="localhost", port=port)
