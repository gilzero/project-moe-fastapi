# main.py
"""
@fileoverview This Python file serves as the main entry point for the FastAPI web application.
@filepath main.py

This file includes:
- Route definitions for the web application.
- Integration with Jinja2 templates for rendering HTML responses.
- Handling of user queries and invoking the analysis workflow.
"""

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from utils import run_full_workflow, workflow_manager
from models import WorkflowResults
import logging
from fastapi.staticfiles import StaticFiles
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from request_id_middleware import RequestIDMiddleware


app = FastAPI()
app.add_middleware(RequestIDMiddleware)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    Renders the index page with the query form.

    Args:
        request (Request): The request object.

    Returns:
        HTMLResponse: The rendered index page.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze", response_class=HTMLResponse)
async def analyze(request: Request, query: str = Form(...)):
    if len(query) > 1000:
        raise HTTPException(status_code=422, detail="Query too long")
    if not query.strip():
        raise HTTPException(status_code=422, detail="Empty query not allowed")
    try:
        results = await run_full_workflow(query)
        return templates.TemplateResponse("results.html", {
            "request": request,
            "results": results,
            "query": query,
            "markdown_to_html": workflow_manager.markdown_to_html
        })
    except Exception as e:
        logging.error(str(e))
        return HTMLResponse("<h1>Error during analysis</h1>", status_code=500)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"errors": exc.errors()}
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred"}
    )