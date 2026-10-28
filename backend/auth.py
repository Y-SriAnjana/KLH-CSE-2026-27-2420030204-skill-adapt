"""
SkillAdapt - Authentication Module
Provides student registration, authentication, secure password hashing,
session token management, and route protection dependencies.
"""

import os
import json
import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from fastapi import Depends, HTTPException, Header, status
from pydantic import BaseModel, Field

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, "data", "users.json")

# In-memory active session store: token -> { "user_id": str, "username": str, "created_at": datetime }
ACTIVE_SESSIONS: Dict[str, Dict[str, Any]] = {}

# Pydantic Schemas
class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    full_name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., min_length=5, max_length=100)
    learning_level: Optional[str] = "Beginner"

class LoginRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    full_name: str
    learning_level: str
    completed_resources: List[str] = []
    created_at: str

def hash_password(password: str) -> str:
    """Hash password using PBKDF2-HMAC-SHA256 with a unique salt."""
    salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100_000)
    return f"{salt}:{key.hex()}"

def verify_password(stored_password: str, provided_password: str) -> bool:
    """Verify a plain-text password against a stored salt:hash string."""
    try:
        if not stored_password or ":" not in stored_password:
            return False
        salt, key = stored_password.split(":")
        new_key = hashlib.pbkdf2_hmac("sha256", provided_password.encode("utf-8"), salt.encode("utf-8"), 100_000)
        return secrets.compare_digest(key, new_key.hex())
    except Exception:
        return False

def load_users() -> List[Dict[str, Any]]:
    """Safely read all user records from persistent JSON storage."""
    if not os.path.exists(USERS_FILE):
        return []
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_users(users: List[Dict[str, Any]]) -> None:
    """Safely persist all user records to JSON storage."""
    temp_file = f"{USERS_FILE}.tmp"
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)
    os.replace(temp_file, USERS_FILE)

def find_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    users = load_users()
    for u in users:
        if u.get("id") == user_id:
            return u
    return None

def find_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    users = load_users()
    for u in users:
        if u.get("username", "").strip().lower() == username.strip().lower():
            return u
    return None

def create_session_token(user: Dict[str, Any]) -> str:
    """Generate a secure cryptographic session token for the student."""
    token = secrets.token_urlsafe(32)
    ACTIVE_SESSIONS[token] = {
        "user_id": user["id"],
        "username": user["username"],
        "created_at": datetime.now()
    }
    return token

def invalidate_session(token: str) -> bool:
    """Remove session from memory upon logout."""
    if token in ACTIVE_SESSIONS:
        del ACTIVE_SESSIONS[token]
        return True
    return False

def get_current_user(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    """
    FastAPI dependency to authenticate requests using 'Authorization: Bearer <token>' header.
    Validates token presence, expiration, and ensures user exists.
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token is missing. Please log in."
        )

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format. Expected 'Bearer <token>'."
        )

    token = parts[1]
    session = ACTIVE_SESSIONS.get(token)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session has expired or is invalid. Please log in again."
        )

    # Check token age (24 hours expiry)
    age = datetime.now() - session["created_at"]
    if age > timedelta(hours=24):
        del ACTIVE_SESSIONS[token]
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session has timed out. Please log in again."
        )

    user = find_user_by_id(session["user_id"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account no longer exists."
        )

    return user

def register_user(data: RegisterRequest) -> Dict[str, Any]:
    """Register a new student account with validations."""
    clean_username = data.username.strip()
    if find_user_by_username(clean_username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Username '{clean_username}' is already taken. Please choose another."
        )

    users = load_users()
    new_user = {
        "id": f"std_{secrets.token_hex(6)}",
        "username": clean_username,
        "email": data.email.strip().lower(),
        "full_name": data.full_name.strip(),
        "password_hash": hash_password(data.password),
        "learning_level": data.learning_level or "Beginner",
        "completed_resources": [],
        "created_at": datetime.now().isoformat()
    }

    users.append(new_user)
    save_users(users)
    return new_user

def authenticate_user(credentials: LoginRequest) -> Dict[str, Any]:
    """Validate username and password, return user dict if valid."""
    user = find_user_by_username(credentials.username.strip())
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password."
        )

    if not verify_password(user.get("password_hash", ""), credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password."
        )

    return user
