from fastapi import WebSocket

class WebSocketManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connections = {}
        return cls._instance

    def add_connection(self, connection_id: str, websocket: WebSocket):
        self.connections[connection_id] = websocket

    def remove_connection(self, connection_id: str):
        if connection_id in self.connections:
            del self.connections[connection_id]

    def get_connection(self, connection_id: str):
        return self.connections.get(connection_id)

    def get_all_connections_keys(self):
        return len(self.connections.keys())


websocket_manager = WebSocketManager()