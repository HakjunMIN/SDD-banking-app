"""
Pydantic Models (Schemas) for API
Request/Response models for Banking App API
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class AccountBase(BaseModel):
    """Base account schema"""
    account_number: str = Field(..., min_length=1, max_length=20)
    account_name: str = Field(..., min_length=1, max_length=100)
    account_type: str = Field(..., min_length=1, max_length=20)
    balance: float = Field(default=0.0, ge=0)


class AccountCreate(AccountBase):
    """Schema for creating a new account"""
    pass


class AccountResponse(AccountBase):
    """Schema for account API responses"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class TransactionBase(BaseModel):
    """Base transaction schema"""
    transaction_type: str = Field(..., min_length=1, max_length=20)
    amount: float = Field(..., gt=0)
    description: Optional[str] = Field(None, max_length=500)
    recipient_account: Optional[str] = Field(None, max_length=20)


class TransactionCreate(TransactionBase):
    """Schema for creating a new transaction"""
    account_id: int = Field(..., gt=0)


class TransactionResponse(TransactionBase):
    """Schema for transaction API responses"""
    id: int
    account_id: int
    transaction_date: datetime
    balance_after: float
    reference_number: str
    status: str = "completed"
    created_at: datetime
    
    class Config:
        from_attributes = True


class TransactionFilter(BaseModel):
    """Schema for transaction filtering"""
    account_id: Optional[int] = None
    transaction_type: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    min_amount: Optional[float] = Field(None, ge=0)
    max_amount: Optional[float] = Field(None, ge=0)
    description_search: Optional[str] = None
    limit: int = Field(default=50, le=100, ge=1)
    offset: int = Field(default=0, ge=0)


class TransactionSummary(BaseModel):
    """Schema for transaction summary/statistics"""
    total_transactions: int
    total_deposits: float
    total_withdrawals: float
    net_change: float
    period_start: datetime
    period_end: datetime


class CategoryBase(BaseModel):
    """Base category schema"""
    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None
    color: Optional[str] = Field(None, pattern=r'^#[0-9A-Fa-f]{6}$')


class CategoryCreate(CategoryBase):
    """Schema for creating a new category"""
    pass


class CategoryResponse(CategoryBase):
    """Schema for category API responses"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True