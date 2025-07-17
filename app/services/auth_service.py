from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from app.config import settings
from app.models.user import User, UserInDB, UserCreate
from sqlalchemy.orm import Session
from app.db.database import UserDB
import logging

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self):
        self.pwd_context = pwd_context
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES

    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return self.pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode a JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError as e:
            logging.error(f"JWT verification error: {e}")
            return None

    def authenticate_user(self, db: Session, username: str, password: str) -> Optional[UserInDB]:
        """Authenticate a user with username and password"""
        user = db.query(UserDB).filter(UserDB.username == username).first()
        if not user:
            return None
        
        if not self.verify_password(password, user.hashed_password):
            # Increment failed login attempts
            user.failed_login_attempts += 1
            if user.failed_login_attempts >= 5:
                user.locked_until = datetime.utcnow() + timedelta(minutes=30)
            db.commit()
            return None
        
        # Reset failed login attempts on successful login
        user.failed_login_attempts = 0
        user.last_login = datetime.utcnow()
        user.locked_until = None
        db.commit()
        
        return UserInDB.from_orm(user)

    def create_user(self, db: Session, user_create: UserCreate) -> UserInDB:
        """Create a new user"""
        hashed_password = self.hash_password(user_create.password)
        db_user = UserDB(
            username=user_create.username,
            email=user_create.email,
            full_name=user_create.full_name,
            hashed_password=hashed_password,
            role=user_create.role.value
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return UserInDB.from_orm(db_user)

    def get_user_by_username(self, db: Session, username: str) -> Optional[UserInDB]:
        """Get user by username"""
        user = db.query(UserDB).filter(UserDB.username == username).first()
        return UserInDB.from_orm(user) if user else None

    def get_user_by_email(self, db: Session, email: str) -> Optional[UserInDB]:
        """Get user by email"""
        user = db.query(UserDB).filter(UserDB.email == email).first()
        return UserInDB.from_orm(user) if user else None

# Create service instance
auth_service = AuthService()

# Convenience functions for backward compatibility
def hash_password(password: str) -> str:
    return auth_service.hash_password(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return auth_service.verify_password(plain_password, hashed_password)

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    return auth_service.create_access_token(data, expires_delta)

def verify_token(token: str) -> Optional[Dict[str, Any]]:
    return auth_service.verify_token(token)