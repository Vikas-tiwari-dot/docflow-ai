import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

logger=logging.getLogger("docflow")

def error_payload(code, message): return {"success":False,"error":{"code":code,"message":message}}
async def validation_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content=error_payload("VALIDATION_ERROR","Request validation failed."))
async def sqlalchemy_handler(request: Request, exc: SQLAlchemyError):
    logger.exception("Database error")
    return JSONResponse(status_code=500, content=error_payload("DATABASE_ERROR","A database error occurred."))
async def generic_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error")
    return JSONResponse(status_code=500, content=error_payload("INTERNAL_ERROR","An unexpected server error occurred."))
