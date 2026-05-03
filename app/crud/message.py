from app.models.message import Message

def create_message(db, username: str, content: str):
    msg = Message(username=username, content=content)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg
