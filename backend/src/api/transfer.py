"""
Transfer API Router
FastAPI router for transfer operations
"""

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models.schemas import TransferCreate, TransferResponse, BankResponse, TransferValidation
from ..services.transfer_service import TransferService

router = APIRouter(prefix="/api/v1/transfers", tags=["transfers"])

# Dependency injection for transfer service
def get_transfer_service(db: Session = Depends(get_db)) -> TransferService:
    return TransferService(db)


@router.post("/", response_model=TransferResponse, status_code=status.HTTP_201_CREATED)
async def create_transfer(
    transfer_data: TransferCreate,
    service: TransferService = Depends(get_transfer_service)
):
    """
    Execute a new transfer
    
    Args:
        transfer_data: Transfer request data
        service: Transfer service dependency
        
    Returns:
        TransferResponse: Created transfer details
        
    Raises:
        HTTPException: 400 for validation errors, 500 for server errors
    """
    try:
        # Determine transfer type based on to_bank_id
        if transfer_data.to_bank_id is None:
            # Internal transfer (same bank)
            transfer = service.create_internal_transfer(
                from_account_id=transfer_data.from_account_id,
                to_account_number=transfer_data.to_account_number,
                amount=transfer_data.amount,
                description=transfer_data.description
            )
        else:
            # External transfer - not implemented in Phase 3
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED,
                detail="External transfers not implemented yet"
            )
        
        return transfer
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Transfer execution failed: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/", response_model=List[TransferResponse])
async def get_transfers(
    account_id: Optional[int] = None,
    status: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    service: TransferService = Depends(get_transfer_service)
):
    """
    Get transfer history
    
    Args:
        account_id: Optional account ID filter
        status: Optional status filter
        limit: Maximum number of records (default: 50)
        offset: Number of records to skip (default: 0)
        service: Transfer service dependency
        
    Returns:
        List[TransferResponse]: List of transfer records
        
    Raises:
        HTTPException: 400 for invalid parameters
    """
    try:
        # Validate parameters
        if limit < 1 or limit > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Limit must be between 1 and 100"
            )
        
        if offset < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Offset must be non-negative"
            )
        
        if not account_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="account_id is required"
            )
        
        # Get transfers from service
        transfers = service.get_transfers_by_account(
            account_id=account_id,
            status=status,
            limit=limit,
            offset=offset
        )
        
        return transfers
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve transfers: {str(e)}"
        )


@router.get("/{transfer_id}", response_model=TransferResponse)
async def get_transfer(
    transfer_id: int,
    service: TransferService = Depends(get_transfer_service)
):
    """
    Get transfer details by ID
    
    Args:
        transfer_id: Transfer ID to retrieve
        service: Transfer service dependency
        
    Returns:
        TransferResponse: Transfer details
        
    Raises:
        HTTPException: 404 if transfer not found
    """
    try:
        # Validate transfer_id
        if transfer_id < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Transfer ID must be positive"
            )
        
        # Get transfer from service
        transfer = service.get_transfer_by_id(transfer_id)
        
        if not transfer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Transfer with ID {transfer_id} not found"
            )
        
        return transfer
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve transfer: {str(e)}"
        )


@router.get("/banks", response_model=List[BankResponse])
async def get_banks(
    service: TransferService = Depends(get_transfer_service)
):
    """
    Get list of supported virtual banks
    Implementation will be added in Phase 4 (User Story 2)
    """
    # TODO: Implement in Phase 4
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Bank listing not implemented yet"
    )


@router.get("/{transfer_id}/status")
async def get_transfer_status(
    transfer_id: int,
    service: TransferService = Depends(get_transfer_service)
):
    """
    Get transfer status
    Implementation will be added in Phase 5 (User Story 3)
    """
    # TODO: Implement in Phase 5
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Transfer status check not implemented yet"
    )


@router.post("/validate", response_model=TransferValidation)
async def validate_transfer(
    transfer_data: TransferCreate,
    service: TransferService = Depends(get_transfer_service)
):
    """
    Validate transfer before execution
    Implementation will be added in Phase 5 (User Story 3)
    """
    # TODO: Implement in Phase 5
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Transfer validation not implemented yet"
    )


@router.get("/accounts/{account_id}/transfer-limits")
async def get_transfer_limits(
    account_id: int,
    service: TransferService = Depends(get_transfer_service)
):
    """
    Get transfer limits for an account
    Implementation will be added in Phase 5 (User Story 3)
    """
    # TODO: Implement in Phase 5
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Transfer limits check not implemented yet"
    )