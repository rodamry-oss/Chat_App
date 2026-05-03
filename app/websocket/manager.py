from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections = {}  # username: websocket

    async def connect(self, username: str, ws: WebSocket):
        self.active_connections[username] = ws

    def disconnect(self, username: str):
        self.active_connections.pop(username, None)

    async def send_private(self, to_user: str, message: str):
        ws = self.active_connections.get(to_user)
        if ws:
            await ws.send_text(message)

manager = ConnectionManager()            