from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from jose import jwt, JWTError
from app.websocket.manager import manager
from app.core.security import SECRET_KEY, ALGORITHM
from app.schemas.ws import IncomingMessage
from pydantic import ValidationError

router = APIRouter()

@router.websocket("/ws")
async def chat(ws: WebSocket):

    token = ws.query_params.get("token")

    if not token:
        await ws.close(code=1008)
        return

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            await ws.close(code=1008)
            return

    except JWTError:
        await ws.close(code=1008)
        return

    await ws.accept()

    await manager.connect(username, ws)

    try:
        while True:
            raw = await ws.receive_text()

            try:
                msg = IncomingMessage.model_validate_json(raw)
            except ValidationError:
                await ws.send_json({"error": "expected {to, body}"})
                continue

            if msg.to not in manager.active_connections:
                await ws.send_json({"error": f"{msg.to} offline"})
                continue

            await manager.send_private(
                msg.to,
                {
                    "from": username,
                    "body": msg.body
                }
            )

            await ws.send_json({
                "to": msg.to,
                "body": msg.body
            })

    except WebSocketDisconnect:
        manager.disconnect(username)