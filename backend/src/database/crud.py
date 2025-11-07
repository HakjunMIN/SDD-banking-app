"""
Database Utilities
Helper functions for database operations
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.database_models import Account, Transaction, TransactionCategory
from ..models.schemas import TransactionFilter


def get_account_by_number(db: Session, account_number: str) -> Optional[Account]:
    """Get account by account number"""
    return db.query(Account).filter(Account.account_number == account_number).first()


def get_account_by_id(db: Session, account_id: int) -> Optional[Account]:
    """Get account by ID"""
    return db.query(Account).filter(Account.id == account_id).first()


def get_transactions_by_account(
    db: Session, 
    account_id: int, 
    filters: Optional[TransactionFilter] = None
) -> List[Transaction]:
    """Get transactions for a specific account with optional filters"""
    query = db.query(Transaction).filter(Transaction.account_id == account_id)
    
    if filters:
        if filters.transaction_type:
            query = query.filter(Transaction.transaction_type == filters.transaction_type)
        if filters.date_from:
            query = query.filter(Transaction.transaction_date >= filters.date_from)
        if filters.date_to:
            query = query.filter(Transaction.transaction_date <= filters.date_to)
        if filters.min_amount:
            query = query.filter(Transaction.amount >= filters.min_amount)
        if filters.max_amount:
            query = query.filter(Transaction.amount <= filters.max_amount)
        if filters.description_search:
            query = query.filter(Transaction.description.contains(filters.description_search))
    
    # Order by transaction date (newest first)
    query = query.order_by(Transaction.transaction_date.desc())
    
    # Apply pagination
    if filters:
        query = query.offset(filters.offset).limit(filters.limit)
    else:
        query = query.limit(50)  # Default limit
    
    return query.all()


def get_transaction_by_id(db: Session, transaction_id: int) -> Optional[Transaction]:
    """Get transaction by ID"""
    return db.query(Transaction).filter(Transaction.id == transaction_id).first()


def get_all_categories(db: Session) -> List[TransactionCategory]:
    """Get all transaction categories"""
    return db.query(TransactionCategory).all()


def get_category_by_name(db: Session, name: str) -> Optional[TransactionCategory]:
    """Get category by name"""
    return db.query(TransactionCategory).filter(TransactionCategory.name == name).first()