"""
Transfer Models for Banking App
SQLAlchemy ORM models for transfer functionality
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database.connection import Base


class Transfer(Base):
    """Transfer model for banking transfers"""
    __tablename__ = "transfers"
    
    id = Column(Integer, primary_key=True, index=True)
    from_account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False, index=True)
    to_account_number = Column(String(20), nullable=False, index=True)
    to_bank_id = Column(Integer, ForeignKey('virtual_banks.id'), nullable=True, index=True)  # None for internal transfers
    amount = Column(Float, nullable=False)
    description = Column(Text)
    status = Column(String(20), default="PENDING", nullable=False)  # PENDING, IN_PROGRESS, COMPLETED, FAILED, CANCELLED
    transfer_type = Column(String(20), nullable=False)  # INTERNAL, EXTERNAL
    reference_number = Column(String(50), unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    error_message = Column(Text)
    
    # Relationships
    virtual_bank = relationship("VirtualBank", back_populates="transfers")
    
    def __repr__(self):
        return f"<Transfer(id={self.id}, amount={self.amount}, status={self.status})>"
    
    def to_dict(self):
        """Convert transfer to dictionary for API responses"""
        return {
            'id': self.id,
            'from_account_id': self.from_account_id,
            'to_account_number': self.to_account_number,
            'to_bank_id': self.to_bank_id,
            'amount': self.amount,
            'description': self.description,
            'status': self.status,
            'transfer_type': self.transfer_type,
            'reference_number': self.reference_number,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'error_message': self.error_message
        }