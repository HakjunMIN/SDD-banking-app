"""
Database Models for Banking App
SQLAlchemy ORM models for transaction history
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from ..database import Base


class Account(Base):
    """Account model for banking accounts"""
    __tablename__ = "accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String(20), unique=True, index=True, nullable=False)
    account_name = Column(String(100), nullable=False)
    account_type = Column(String(20), nullable=False)  # checking, savings, etc.
    balance = Column(Float, default=0.0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Transaction(Base):
    """Transaction model for banking transactions"""
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, nullable=False, index=True)  # Foreign key to Account
    transaction_type = Column(String(20), nullable=False)  # deposit, withdrawal, transfer
    amount = Column(Float, nullable=False)
    description = Column(Text)
    recipient_account = Column(String(20))  # For transfers
    transaction_date = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    balance_after = Column(Float, nullable=False)  # Account balance after transaction
    reference_number = Column(String(50), unique=True, index=True)
    status = Column(String(20), default="completed")  # completed, pending, failed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, type={self.transaction_type}, amount={self.amount})>"


class TransactionCategory(Base):
    """Category model for transaction categorization"""
    __tablename__ = "transaction_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    color = Column(String(7))  # Hex color code
    created_at = Column(DateTime(timezone=True), server_default=func.now())