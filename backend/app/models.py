
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON
from sqlalchemy.sql import func
from .db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    role = Column(String, default="parent")
    full_name = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, unique=True, index=True, nullable=False)
    data = Column(JSON)  # store dynamic attributes as JSON
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    deleted = Column(Boolean, default=False)

class AuditEntry(Base):
    __tablename__ = "app_audit"
    id = Column(Integer, primary_key=True)
    table_name = Column(String, nullable=False)
    operation = Column(String, nullable=False)
    changed_by = Column(String, nullable=True)
    changed_at = Column(DateTime(timezone=True), server_default=func.now())
    row_id = Column(String, nullable=True)
    before = Column(JSON, nullable=True)
    after = Column(JSON, nullable=True)
