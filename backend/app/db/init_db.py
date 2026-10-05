from app.db.session import engine, Base
from app.models import user, document, integration, chat

def init_db():
    Base.metadata.create_all(bind=engine)
