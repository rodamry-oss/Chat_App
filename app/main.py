from fastapi import FastAPI
from app.api.routes import auth, chat_ws, users
from app.db.base import Base
from app.db.session import engine
from app.db.base import Base
from app.db.session import engine

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(auth.router, prefix="/auth")
app.include_router(chat_ws.router)
app.include_router(users.router, prefix="/users", tags=["users"])

Base.metadata.create_all(bind=engine)
