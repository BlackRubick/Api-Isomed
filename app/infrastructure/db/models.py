"""
Modelos de SQLAlchemy para MySQL.
"""
from sqlalchemy import Column, Integer, String, DateTime, func, Text
from app.infrastructure.db.database import Base


class UserModel(Base):
    """Modelo de usuario para SQLAlchemy."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    hospital = Column(String(255), nullable=True)
    position = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())