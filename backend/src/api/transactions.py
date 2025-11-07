"""
Transaction API Endpoints
FastAPI routes for transaction operations
"""

import logging
import traceback
from typing import Optional
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database.connection import get_db
from ..services.transaction_service import TransactionService
from ..utils.validators import ValidationUtils, DataUtils

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("/", response_model=dict)
async def get_transactions(
    account_id: Optional[int] = Query(default=1, description="Account ID"),
    type: Optional[str] = Query(default=None, description="Transaction type (deposit, withdrawal, transfer)"),
    from_date: Optional[date] = Query(default=None, description="Start date filter (YYYY-MM-DD)"),
    to_date: Optional[date] = Query(default=None, description="End date filter (YYYY-MM-DD)"),
    limit: int = Query(default=20, ge=1, le=100, description="Maximum number of transactions"),
    offset: int = Query(default=0, ge=0, description="Number of transactions to skip"),
    search: Optional[str] = Query(default=None, description="Search in description or recipient account"),
    sort_by: str = Query(default="transaction_date", description="Sort by field (transaction_date, amount)"),
    sort_order: str = Query(default="desc", description="Sort order (asc, desc)"),
    db: Session = Depends(get_db)
):
    """
    Get transactions with filtering, pagination, and search
    
    Returns transaction list with pagination information and account summary
    """
    logger.info(f"GET /transactions called with: account_id={account_id}, type={type}, from_date={from_date}, to_date={to_date}, limit={limit}, offset={offset}")
    
    try:
        logger.info("Creating TransactionService instance")
        service = TransactionService(db)
        
        # Validate date range if provided
        if from_date and to_date:
            logger.info(f"Validating date range: {from_date} to {to_date}")
            is_valid, error_msg = ValidationUtils.validate_date_range(from_date, to_date)
            if not is_valid:
                logger.error(f"Date range validation failed: {error_msg}")
                raise HTTPException(status_code=400, detail=error_msg)
        
        # Validate transaction type if provided
        if type:
            logger.info(f"Validating transaction type: {type}")
            is_valid, error_msg = ValidationUtils.validate_transaction_type(type)
            if not is_valid:
                logger.error(f"Transaction type validation failed: {error_msg}")
                raise HTTPException(status_code=400, detail=error_msg)
        
        # Search functionality
        if search:
            logger.info(f"Performing search with term: {search}")
            transactions, total_count = service.search_transactions(
                search_term=search,
                account_id=account_id,
                limit=limit,
                offset=offset
            )
        else:
            # Regular filtering
            logger.info(f"Performing regular transaction filtering")
            transactions, total_count = service.get_transactions(
                account_id=account_id,
                transaction_type=type,
                from_date=from_date,
                to_date=to_date,
                limit=limit,
                offset=offset,
                sort_by=sort_by,
                sort_order=sort_order
            )
        
        logger.info(f"Found {len(transactions)} transactions, total count: {total_count}")
        
        # Convert to response format
        transaction_data = []
        for transaction in transactions:
            transaction_data.append({
                "id": transaction.id,
                "account_id": transaction.account_id,
                "transaction_date": transaction.transaction_date.isoformat(),
                "transaction_type": transaction.transaction_type,
                "amount": float(transaction.amount),
                "description": transaction.description,
                "recipient_account": transaction.recipient_account,
                "balance_after": float(transaction.balance_after),
                "reference_number": transaction.reference_number,
                "status": transaction.status,
                "created_at": transaction.created_at.isoformat()
            })
        
        # Create pagination info
        pagination_info = {
            "current_page": offset // limit + 1,
            "total_pages": (total_count + limit - 1) // limit,
            "page_size": limit,
            "total_items": total_count,
            "has_next": offset + limit < total_count,
            "has_previous": offset > 0
        }
        
        # Get account summary
        account_summary = service.get_account_summary(account_id or 1)
        
        logger.info(f"Successfully returning {len(transaction_data)} transactions")
        
        return {
            "data": transaction_data,
            "pagination": pagination_info,
            "account_info": account_summary.get("account") if account_summary else None,
            "summary": account_summary.get("summary") if account_summary else None
        }
        
    except ValueError as e:
        logger.error(f"ValueError in get_transactions: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in get_transactions: {str(e)}")
        logger.error(f"Exception type: {type(e).__name__}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500, 
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/{transaction_id}", response_model=dict)
async def get_transaction_detail(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    """
    Get detailed information for a specific transaction
    """
    try:
        service = TransactionService(db)
        transaction = service.get_transaction_by_id(transaction_id)
        
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        return {
            "id": transaction.id,
            "account_id": transaction.account_id,
            "transaction_date": transaction.transaction_date.isoformat(),
            "transaction_type": transaction.transaction_type,
            "amount": float(transaction.amount),
            "description": transaction.description,
            "recipient_account": transaction.recipient_account,
            "balance_after": float(transaction.balance_after),
            "reference_number": transaction.reference_number,
            "status": transaction.status,
            "created_at": transaction.created_at.isoformat(),
            # Additional formatted fields for display
            "formatted_amount": f"{transaction.amount:,.0f}원",
            "formatted_balance": f"{transaction.balance_after:,.0f}원",
            "formatted_date": transaction.transaction_date.strftime("%Y년 %m월 %d일 %H시 %M분"),
            "type_icon": "↑" if transaction.transaction_type == "deposit" else "↓" if transaction.transaction_type == "withdrawal" else "→"
        }
        
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/statistics/{account_id}")
async def get_transaction_statistics(
    account_id: int,
    period_days: int = Query(default=30, ge=1, le=365, description="Analysis period in days"),
    db: Session = Depends(get_db)
):
    """
    Get transaction statistics for specified account and period
    """
    try:
        service = TransactionService(db)
        statistics = service.get_transaction_statistics(account_id, period_days)
        
        return statistics
        
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")