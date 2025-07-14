from fastapi import HTTPException
from app.services.auth_service import hash_password, verify_password
from app.models.user import User
from typing import Dict

# Fake in-memory store for demonstration
users_db: Dict[str, str] = {}

def login(user: User):
    stored = users_db.get(user.username)
    if not stored or not verify_password(user.password, stored):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": "fake-jwt-token", "token_type": "bearer"}

def signup(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    users_db[user.username] = hash_password(user.password)
    return {"message": "User created"}
