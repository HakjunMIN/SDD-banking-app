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


# Transfer-related schemas
class TransferBase(BaseModel):
    """Base transfer schema"""
    to_account_number: str = Field(..., min_length=1, max_length=20)
    amount: float = Field(..., gt=0, le=1000000)  # Max 1M KRW
    description: Optional[str] = Field(None, max_length=500)


class TransferCreate(TransferBase):
    """Schema for creating a new transfer"""
    from_account_id: int = Field(..., gt=0)
    to_bank_id: Optional[int] = Field(None, gt=0)  # None for internal transfers


class TransferResponse(TransferBase):
    """Schema for transfer API responses"""
    id: int
    from_account_id: int
    to_bank_id: Optional[int] = None
    status: str
    transfer_type: str
    reference_number: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    
    class Config:
        from_attributes = True


class BankResponse(BaseModel):
    """Schema for bank API responses"""
    id: int
    name: str
    code: str
    description: Optional[str] = None
    
    class Config:
        from_attributes = True


class TransferValidation(BaseModel):
    """Schema for transfer validation responses"""
    is_valid: bool
    errors: Optional[list[str]] = None
    warnings: Optional[list[str]] = None
    estimated_fee: Optional[float] = None