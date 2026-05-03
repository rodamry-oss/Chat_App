from pydantic import BaseModel

class MessageCreate(BaseModel):
    content: str

class MessageOut(BaseModel):
    id: int
    content: str
    user_id: int   

    class Config:
        from_attributes = True