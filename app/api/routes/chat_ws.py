from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from jose import jwt, JWTError
from app.websocket.manager import manager
from app.core.security import SECRET_KEY, ALGORITHM

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
            data = await ws.receive_text()

            try:
                to_user, message = data.split(":", 1)
            except ValueError:
                await ws.send_text("format: username:message")
                continue

            if to_user not in manager.active_connections:
                await ws.send_text(f"{to_user} Offline")
                continue

            await manager.send_private(
                to_user,
                f"(Private) {username}: {message}"
            )

            await ws.send_text(f"You → {to_user}: {message}")

    except WebSocketDisconnect:
        manager.disconnect(username)