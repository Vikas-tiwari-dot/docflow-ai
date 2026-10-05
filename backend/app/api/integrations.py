import secrets
from urllib.parse import urlencode
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import Integration, Document, DocumentChunk
from app.core.deps import get_current_user
from app.core.config import get_settings
from app.connectors.google_drive import GoogleDriveConnector
from app.services.document_processor import extract, sha256, chunk_text
router=APIRouter(prefix="/api/integrations",tags=["Integrations"])
@router.get("")
def integrations(user=Depends(get_current_user),db:Session=Depends(get_db)):
    providers={"google_drive":False}
    for i in db.query(Integration).filter(Integration.user_id==user.id).all(): providers[i.provider]=True
    return providers
@router.get("/google/connect")
def google_connect(user=Depends(get_current_user)):
    s=get_settings()
    if not s.google_client_id or not s.google_client_secret: raise HTTPException(503,{"success":False,"error":{"code":"GOOGLE_NOT_CONFIGURED","message":"Google OAuth is not configured on this environment."}})
    state=f"{user.id}:{secrets.token_urlsafe(16)}"
    params={"client_id":s.google_client_id,"redirect_uri":s.google_redirect_uri,"response_type":"code","scope":"https://www.googleapis.com/auth/drive.readonly","access_type":"offline","prompt":"consent","state":state}
    return {"authorization_url":"https://accounts.google.com/o/oauth2/v2/auth?"+urlencode(params)}
@router.get("/google/callback")
def google_callback(code:str,state:str,db:Session=Depends(get_db)):
    s=get_settings()
    try: user_id=int(state.split(":",1)[0])
    except: raise HTTPException(400,"Invalid OAuth state")
    from google_auth_oauthlib.flow import Flow
    flow=Flow.from_client_config({"web":{"client_id":s.google_client_id,"client_secret":s.google_client_secret,"auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token"}},scopes=["https://www.googleapis.com/auth/drive.readonly"],redirect_uri=s.google_redirect_uri)
    flow.fetch_token(code=code); creds=flow.credentials
    item=db.query(Integration).filter(Integration.user_id==user_id,Integration.provider=="google_drive").first()
    if not item: item=Integration(user_id=user_id,provider="google_drive"); db.add(item)
    item.access_token=creds.token; item.refresh_token=creds.refresh_token; item.expires_at=creds.expiry; db.commit()
    return RedirectResponse(s.frontend_url+"/integrations?connected=1")
@router.post("/google/import")
def google_import(user=Depends(get_current_user),db:Session=Depends(get_db)):
    item=db.query(Integration).filter(Integration.user_id==user.id,Integration.provider=="google_drive").first()
    if not item or not item.access_token: raise HTTPException(400,{"success":False,"error":{"code":"GOOGLE_NOT_CONNECTED","message":"Connect Google Drive first."}})
    try: connector=GoogleDriveConnector(item.access_token,item.refresh_token); files=connector.list_files()
    except Exception: raise HTTPException(502,{"success":False,"error":{"code":"GOOGLE_API_ERROR","message":"Unable to access Google Drive."}})
    imported=0; skipped=0
    for meta in files:
        try:
            m,data=connector.download_file(meta["id"]); h=sha256(data)
            if db.query(Document).filter(Document.user_id==user.id,Document.content_hash==h).first(): skipped+=1; continue
            ext="pdf" if m["mimeType"]=="application/pdf" else "docx"; text=extract(data,ext)
            if not text: continue
            d=Document(user_id=user.id,filename=m["name"],file_type=ext,file_size=len(data),extracted_text=text,status="completed",content_hash=h)
            d.chunks=[DocumentChunk(chunk_index=i,content=c) for i,c in enumerate(chunk_text(text))]; db.add(d); imported+=1
        except Exception: db.rollback(); continue
    db.commit(); return {"success":True,"imported":imported,"skipped":skipped}
@router.delete("/google/disconnect")
def google_disconnect(user=Depends(get_current_user),db:Session=Depends(get_db)):
    item=db.query(Integration).filter(Integration.user_id==user.id,Integration.provider=="google_drive").first()
    if item: db.delete(item); db.commit()
    return {"success":True}
