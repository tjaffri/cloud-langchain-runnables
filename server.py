import os
import logging
from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from typing_extensions import Annotated
from langserve import add_routes
from runnables.add_one import add_one_runnable
from runnables.resume_key_points import resume_key_points_runnable
from runnables.resume_summary import resume_summary_runnable

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def verify_token(x_token: Annotated[str, Header()]) -> None:
    """Verify the token is valid."""
    # Replace this with your actual authentication logic
    if x_token != os.getenv("SECRET"):
        raise HTTPException(status_code=400, detail="X-Token header invalid")


app = FastAPI(
    title="LangChain Server",
    description="Sample LangChain Server exposing runnables deployed via Railway.app",
    version="1.0",
    dependencies=[Depends(verify_token)],
)


@app.middleware("http")
async def log_request_body(request: Request, call_next):
    body = await request.body()
    logger.info(f"Request body: {body.decode('utf-8')}")
    response = await call_next(request)
    return response


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc}")
    logger.error(f"Request body: {await request.body()}")
    return await request_validation_exception_handler(request, exc)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP exception: {exc.detail}")
    logger.error(f"Request body: {await request.body()}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


add_routes(app, add_one_runnable, path="/add_one")
add_routes(app, resume_key_points_runnable, path="/resume_key_points")
add_routes(app, resume_summary_runnable, path="/resume_summary")

if __name__ == "__main__":
    import uvicorn

    port = 8000
    port_env = os.getenv("PORT")
    if port_env:
        port = int(port_env)

    uvicorn.run(app, host="0.0.0.0", port=port)
