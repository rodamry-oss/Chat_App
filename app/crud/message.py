from app.models.message import Message


def create_message(db, from_user: str, to_user: str, content: str) -> Message:
    msg = Message(from_user=from_user, to_user=to_user, content=content)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg
