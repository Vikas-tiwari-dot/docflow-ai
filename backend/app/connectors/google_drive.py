import io
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from app.connectors.base import BaseConnector
SCOPES=["https://www.googleapis.com/auth/drive.readonly"]
class GoogleDriveConnector(BaseConnector):
    def __init__(self, access_token, refresh_token=None):
        self.creds=Credentials(token=access_token, refresh_token=refresh_token, scopes=SCOPES)
        self.service=build("drive","v3",credentials=self.creds,cache_discovery=False)
    def authenticate(self, **kwargs): return True
    def list_files(self):
        q="trashed=false and (mimeType='application/pdf' or mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document')"
        return self.service.files().list(q=q,fields="files(id,name,mimeType,size,modifiedTime)",pageSize=100).execute().get("files",[])
    def get_file_metadata(self,file_id): return self.service.files().get(fileId=file_id,fields="id,name,mimeType,size,modifiedTime").execute()
    def download_file(self,file_id):
        meta=self.get_file_metadata(file_id); request=self.service.files().get_media(fileId=file_id); buf=io.BytesIO(); downloader=MediaIoBaseDownload(buf,request)
        done=False
        while not done: _,done=downloader.next_chunk()
        return meta,buf.getvalue()
    def disconnect(self): self.creds=None; self.service=None
