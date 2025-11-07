"""
Account API Endpoints
FastAPI routes for account operations
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database.connection import get_db
from ..services.transaction_service import AccountService, TransactionService
from ..utils.validators import ValidationUtils

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("/{account_id}")
async def get_account_detail(
    account_id: int,
    db: Session = Depends(get_db)
):
    """
    Get detailed account information including summary statistics
    """
    try:
        account_service = AccountService(db)
        transaction_service = TransactionService(db)
        
        # Get basic account info
        account = account_service.get_account_by_id(account_id)
        
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        
        # Get account summary with transaction statistics
        account_summary = transaction_service.get_account_summary(account_id)
        
        return {
            "account": {
                "id": account.id,
                "account_number": account.account_number,
                "account_name": account.account_name,
                "account_type": account.account_type,
                "balance": float(account.balance),
                "formatted_balance": f"{account.balance:,.0f}원",
                "created_at": account.created_at.isoformat(),
                "updated_at": account.updated_at.isoformat() if account.updated_at else None,
                # Security: mask account number for display
                "masked_account_number": ValidationUtils.mask_account_number(account.account_number)
            },
            "summary": account_summary.get("summary") if account_summary else None
        }
        
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/")
async def get_accounts(
    limit: int = Query(default=10, ge=1, le=50, description="Maximum number of accounts"),
    offset: int = Query(default=0, ge=0, description="Number of accounts to skip"),
    db: Session = Depends(get_db)
):
    """
    Get list of accounts (for prototype - normally would be user-specific)
    """
    try:
        service = AccountService(db)
        accounts, total_count = service.get_accounts(limit=limit, offset=offset)
        
        account_data = []
        for account in accounts:
            account_data.append({
                "id": account.id,
                "account_number": account.account_number,
                "account_name": account.account_name,
                "account_type": account.account_type,
                "balance": float(account.balance),
                "formatted_balance": f"{account.balance:,.0f}원",
                "masked_account_number": ValidationUtils.mask_account_number(account.account_number),
                "created_at": account.created_at.isoformat()
            })
        
        return {
            "data": account_data,
            "pagination": {
                "current_page": offset // limit + 1,
                "total_pages": (total_count + limit - 1) // limit,
                "page_size": limit,
                "total_items": total_count,
                "has_next": offset + limit < total_count,
                "has_previous": offset > 0
            }
        }
        
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{account_id}/balance")
async def get_account_balance(
    account_id: int,
    db: Session = Depends(get_db)
):
    """
    Get current account balance
    """
    try:
        service = AccountService(db)
        account = service.get_account_by_id(account_id)
        
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        
        return {
            "account_id": account.id,
            "balance": float(account.balance),
            "formatted_balance": f"{account.balance:,.0f}원",
            "account_name": account.account_name,
            "last_updated": account.updated_at.isoformat() if account.updated_at else account.created_at.isoformat()
        }
        
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")