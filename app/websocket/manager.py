from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, set[WebSocket]] = {}

    async def connect(self, username: str, ws: WebSocket):
        self.active_connections.setdefault(username, set()).add(ws)

    def disconnect(self, username: str, ws: WebSocket):
        conns = self.active_connections.get(username)
        if not conns:
            return
        conns.discard(ws)
        if not conns:
            self.active_connections.pop(username, None)

    async def send_private(self, to_user: str, message):
        for ws in list(self.active_connections.get(to_user, ())):
            await ws.send_json(message) if isinstance(message, dict) else await ws.send_text(message)

    def is_online(self, username: str) -> bool:
        return bool(self.active_connections.get(username))

manager = ConnectionManager()          