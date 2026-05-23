from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from routes.video_route import router as video_router

app = FastAPI()

@app.get("/")
def welcome():
    return "Hello"

app.include_router(router=video_router, prefix="/api/videos", tags=["Videos"])

@app.exception_handler(HTTPException)
def exception_handler(request: Request ,exception: HTTPException):
    return JSONResponse(
        content=exception.detail if exception.detail else "Some error occured",
        status_code=exception.status_code
    )

@app.exception_handler(RequestValidationError)
def validation_handler(request: Request, exception: RequestValidationError):
    return JSONResponse(
        content={"detail": exception.errors()},
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
    )