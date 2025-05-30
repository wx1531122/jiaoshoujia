# backend/app/core/error_handlers.py
from fastapi import Request, HTTPException as FastAPIHTTPException
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException # For broader coverage

from app.core.exceptions import DetailedHTTPException # Import your base custom exception

async def detailed_http_exception_handler(request: Request, exc: DetailedHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=exc.headers,
    )

async def fastapi_http_exception_handler(request: Request, exc: FastAPIHTTPException):
    # This handles FastAPI's own HTTPException
    # Useful if you want to ensure a consistent response format for all HTTPExceptions
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=getattr(exc, "headers", None), # FastAPI's HTTPException might not always have headers
    )

async def starlette_http_exception_handler(request: Request, exc: StarletteHTTPException):
    # This handles Starlette's HTTPException, which FastAPI's is based on
    # This can be useful for catching exceptions from middleware or Starlette itself
    # and ensures consistent formatting.
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}, # Starlette's HTTPException also has a detail attribute
        headers=getattr(exc, "headers", None),
    )

# Optional: A generic fallback handler for unexpected errors (500)
# async def generic_exception_handler(request: Request, exc: Exception):
#     # Log the exception here for debugging
#     print(f"Unhandled exception: {exc}") # Replace with actual logging
#     return JSONResponse(
#         status_code=500,
#         content={"detail": "Internal server error"},
#     )
