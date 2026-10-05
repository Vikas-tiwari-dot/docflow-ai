import logging
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.core.errors import validation_handler, sqlalchemy_handler, generic_handler
from app.db.init_db import init_db
from app.api import auth, users, documents, integrations

logging.basicConfig(level=logging.INFO,format="%(asctime)s %(levelname)s %(name)s %(message)s")
s=get_settings(); app=FastAPI(title=s.app_name,version="1.0.0",description="AI document integration and processing SaaS API")
app.add_middleware(CORSMiddleware,allow_origins=s.cors_list,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.add_exception_handler(RequestValidationError,validation_handler)
app.add_exception_handler(SQLAlchemyError,sqlalchemy_handler)
app.add_exception_handler(Exception,generic_handler)
app.include_router(auth.router); app.include_router(users.router); app.include_router(documents.router); app.include_router(integrations.router)
@app.on_event("startup")
def startup(): init_db()
@app.get("/api/health",tags=["System"])
def health(): return {"status":"ok","service":"docflow-api"}
