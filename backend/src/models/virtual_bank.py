"""
Virtual Bank Models for Banking App
SQLAlchemy ORM models for virtual bank interfaces
"""

from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship
from ..database.connection import Base


class VirtualBank(Base):
    """Virtual Bank model for external bank simulation"""
    __tablename__ = "virtual_banks"
    
    id = Column(Integer, primary_key=True, index=True)
    bank_code = Column(String(10), unique=True, index=True, nullable=False)
    bank_name = Column(String(100), nullable=False)
    bank_name_en = Column(String(100), nullable=True)  # English name
    is_active = Column(Boolean, default=True, nullable=False)
    transfer_fee = Column(Integer, default=500)  # Default transfer fee in KRW
    processing_time_min = Column(Integer, default=1)  # Minimum processing time in minutes
    processing_time_max = Column(Integer, default=10)  # Maximum processing time in minutes
    success_rate = Column(Integer, default=95)  # Success rate percentage (for simulation)
    api_endpoint = Column(String(255))  # Virtual API endpoint (for simulation)
    description = Column(Text)
    
    # Relationships
    transfers = relationship("Transfer", back_populates="virtual_bank")
    
    def __repr__(self):
        return f"<VirtualBank(code={self.bank_code}, name={self.bank_name})>"
    
    def to_dict(self):
        """Convert virtual bank to dictionary for API responses"""
        return {
            'id': self.id,
            'bank_code': self.bank_code,
            'bank_name': self.bank_name,
            'bank_name_en': self.bank_name_en,
            'is_active': self.is_active,
            'transfer_fee': self.transfer_fee,
            'processing_time_min': self.processing_time_min,
            'processing_time_max': self.processing_time_max,
            'success_rate': self.success_rate,
            'api_endpoint': self.api_endpoint,
            'description': self.description
        }