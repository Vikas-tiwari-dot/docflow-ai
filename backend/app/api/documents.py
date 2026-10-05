import logging
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import Document, DocumentChunk, ChatHistory
from app.core.deps import get_current_user
from app.core.config import get_settings
from app.schemas.document import DocumentResponse, DocumentDetail, AskRequest, AskResponse, ChatResponse
from app.services.document_processor import extract, sha256, chunk_text
from app.services.ai_service import answer_question
logger=logging.getLogger("docflow.api.documents")
router=APIRouter(prefix="/api/documents",tags=["Documents"])

def owned(db,user,id):
    d=db.query(Document).filter(Document.id==id,Document.user_id==user.id).first()
    if not d: raise HTTPException(404,{"success":False,"error":{"code":"DOCUMENT_NOT_FOUND","message":"Document was not found."}})
    return d
@router.post("/upload",response_model=DocumentResponse,status_code=201)
async def upload(file:UploadFile=File(...),user=Depends(get_current_user),db:Session=Depends(get_db)):
    s=get_settings(); data=await file.read(); size=len(data)
    if size==0: raise HTTPException(400,{"success":False,"error":{"code":"EMPTY_FILE","message":"The uploaded file is empty."}})
    if size>s.max_file_size_mb*1024*1024: raise HTTPException(413,{"success":False,"error":{"code":"FILE_TOO_LARGE","message":f"Maximum file size is {s.max_file_size_mb} MB."}})
    ext=(file.filename or "").lower().rsplit(".",1)[-1] if "." in (file.filename or "") else ""
    if ext not in {"pdf","docx"}: raise HTTPException(400,{"success":False,"error":{"code":"UNSUPPORTED_FILE","message":"Only PDF and DOCX files are supported."}})
    h=sha256(data)
    duplicate=db.query(Document).filter(Document.user_id==user.id,Document.content_hash==h).first()
    if duplicate: raise HTTPException(409,{"success":False,"error":{"code":"DUPLICATE_DOCUMENT","message":"This document has already been uploaded."}})
    d=Document(user_id=user.id,filename=file.filename,file_type=ext,file_size=size,status="processing",content_hash=h); db.add(d); db.commit(); db.refresh(d)
    try:
        text=extract(data,ext)
        if not text: raise ValueError("No text could be extracted from document")
        d.extracted_text=text; d.status="completed"
        for i,c in enumerate(chunk_text(text)): d.chunks.append(DocumentChunk(chunk_index=i,content=c))
        db.commit(); db.refresh(d); logger.info("document_processed user=%s document=%s",user.id,d.id)
        return d
    except Exception:
        db.rollback(); d=db.get(Document,d.id); d.status="failed"; db.commit(); logger.exception("document_processing_failed document=%s",d.id)
        raise HTTPException(422,{"success":False,"error":{"code":"EXTRACTION_FAILED","message":"Document processing failed. Check that the file is valid and contains extractable text."}})
@router.get("",response_model=list[DocumentResponse])
def list_documents(search:str|None=Query(None),user=Depends(get_current_user),db:Session=Depends(get_db)):
    q=db.query(Document).filter(Document.user_id==user.id)
    if search: q=q.filter(Document.filename.ilike(f"%{search}%"))
    return q.order_by(Document.created_at.desc()).all()
@router.get("/{id}",response_model=DocumentDetail)
def get_document(id:int,user=Depends(get_current_user),db:Session=Depends(get_db)): return owned(db,user,id)
@router.delete("/{id}")
def delete_document(id:int,user=Depends(get_current_user),db:Session=Depends(get_db)):
    d=owned(db,user,id); db.delete(d); db.commit(); return {"success":True}
@router.post("/{id}/ask",response_model=AskResponse)
def ask(id:int,payload:AskRequest,user=Depends(get_current_user),db:Session=Depends(get_db)):
    d=owned(db,user,id)
    if d.status!="completed": raise HTTPException(422,{"success":False,"error":{"code":"DOCUMENT_NOT_READY","message":"Document is not ready for AI questions."}})
    try: ans=answer_question(payload.question,d.chunks and [c.content for c in d.chunks] or [d.extracted_text])
    except RuntimeError as e: raise HTTPException(502,{"success":False,"error":{"code":"AI_PROVIDER_ERROR","message":str(e)}})
    chat=ChatHistory(document_id=d.id,question=payload.question,answer=ans); db.add(chat); db.commit()
    return {"answer":ans,"document_id":d.id,"question":payload.question}
@router.get("/{id}/chat",response_model=list[ChatResponse])
def chat(id:int,user=Depends(get_current_user),db:Session=Depends(get_db)):
    d=owned(db,user,id); return db.query(ChatHistory).filter(ChatHistory.document_id==d.id).order_by(ChatHistory.created_at.asc()).all()
