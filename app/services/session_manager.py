import uuid
import time
import threading

class SessionManager:
    def __init__(self, store=None, expiry_seconds=3600):
        self._lock = threading.RLock()
        self.store = store or {}
        self.expiry_seconds = expiry_seconds

    def create_session(self, user_id, metadata=None):
        session_id = str(uuid.uuid4())
        timestamp = time.time()
        with self._lock:
            self.store[session_id] = {
                "user_id": user_id,
                "created_at": timestamp,
                "last_active": timestamp,
                "metadata": metadata or {}
            }
        return session_id

    def get_session(self, session_id):
        with self._lock:
            session = self.store.get(session_id)
            if session is None:
                return None
            if time.time() - session["last_active"] >= self.expiry_seconds:
               
                del self.store[session_id]
                return None
            return session.copy()  

    def update_metadata(self, session_id, key, value):
        with self._lock:
            session = self.get_session(session_id)
            if session is not None:
           
                self.store[session_id]["metadata"][key] = value
                self.store[session_id]["last_active"] = time.time()

    def touch_session(self, session_id):
        with self._lock:
            session = self.get_session(session_id)
            if session is not None:
                self.store[session_id]["last_active"] = time.time()

    def invalidate_session(self, session_id):
        with self._lock:
            if session_id in self.store:
                del self.store[session_id]

    def cleanup_expired_sessions(self):
        with self._lock:
            now = time.time()
            expired_sessions = [
                sid for sid, session in self.store.items()
                if now - session["last_active"] >= self.expiry_seconds
            ]
            for sid in expired_sessions:
                del self.store[sid]

    def get_active_user_ids(self):
        with self._lock:
            now = time.time()
            user_ids = {
                session["user_id"]
                for session in self.store.values()
                if now - session["last_active"] < self.expiry_seconds
            }
            return list(user_ids)

