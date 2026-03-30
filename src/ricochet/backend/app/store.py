from typing import Dict
from uuid import uuid4


class InMemorySessionStore:
    def __init__(self):
        self.sessions: Dict[str, object] = {}

    def create(self, session_obj):
        session_id = str(uuid4())
        self.sessions[session_id] = session_obj
        return session_id

    def get(self, session_id: str):
        return self.sessions.get(session_id)


store = InMemorySessionStore()