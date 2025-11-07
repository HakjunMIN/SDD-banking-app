"""
Transfer Service
Business logic for transfer operations
"""

from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
from ..models.transfer import Transfer
from ..models.virtual_bank import VirtualBank
from ..models.database_models import Account, Transaction
from .bank_interface import BankInterface


class TransferService:
    """Service class for handling transfer operations"""
    
    def __init__(self, db: Session):
        self.db = db
        self.bank_interface = BankInterface(db)
    
    def create_internal_transfer(self, from_account_id: int, to_account_number: str, 
                               amount: float, description: Optional[str] = None) -> Transfer:
        """
        Create internal transfer between accounts in the same bank
        
        Args:
            from_account_id: Source account ID
            to_account_number: Destination account number
            amount: Transfer amount
            description: Optional transfer description
            
        Returns:
            Transfer: Created transfer record
            
        Raises:
            ValueError: If validation fails
            RuntimeError: If transfer execution fails
        """
        try:
            print(f"Creating internal transfer: from_account_id={from_account_id}, to_account_number={to_account_number}, amount={amount}, description={description}")
            # Validate amount
            if amount <= 0:
                raise ValueError("Transfer amount must be positive")
            if amount > 1000000:  # 1M KRW limit
                raise ValueError("Transfer amount exceeds maximum limit")
            
            # Check if source account exists and has sufficient balance
            if not self._check_account_balance(from_account_id, amount):
                raise ValueError("Insufficient balance")
            
            # Find destination account to get recipient name
            to_account = self.db.query(Account).filter(
                Account.account_number == to_account_number
            ).first()
            
            if not to_account:
                raise ValueError("Destination account not found")
            
            # Prevent self-transfer
            from_account = self.db.query(Account).filter(
                Account.id == from_account_id
            ).first()
            
            if not from_account:
                raise ValueError("Source account not found")
                
            if from_account.account_number == to_account_number:
                raise ValueError("Cannot transfer to the same account")
            
            # Create transfer record
            transfer = Transfer(
                from_account_id=from_account_id,
                to_account_number=to_account_number,
                amount=amount,
                status="PENDING",
                description=description,
                transfer_type="INTERNAL",
                reference_number=self._generate_reference_number()
            )
            
            self.db.add(transfer)
            self.db.flush()  # Get transfer ID
            
            # Execute the transfer
            self._execute_internal_transfer(transfer)
            
            self.db.commit()
            return transfer
            
        except Exception as e:
            self.db.rollback()
            # Update transfer status to failed if it was created
            if 'transfer' in locals():
                transfer.status = "FAILED"
                transfer.error_message = str(e)
                transfer.completed_at = datetime.now()
                self.db.commit()
            raise
    
    def create_external_transfer(self, from_account_id: int, to_account_number: str,
                               to_bank_id: int, amount: float, 
                               description: Optional[str] = None) -> Transfer:
        """
        Create external transfer to another bank via virtual interface
        Implementation will be added in Phase 4 (User Story 2)
        """
        # TODO: Implement in Phase 4
        raise NotImplementedError("External transfer not implemented yet")
    
    def validate_transfer(self, from_account_id: int, amount: float) -> Dict[str, Any]:
        """
        Validate transfer requirements (balance, limits, account status)
        Implementation will be added in Phase 5 (User Story 3)
        """
        # TODO: Implement in Phase 5
        raise NotImplementedError("Transfer validation not implemented yet")
    
    def get_transfers_by_account(self, account_id: int, 
                               status: Optional[str] = None,
                               limit: int = 50, offset: int = 0) -> List[Transfer]:
        """
        Get transfer history for an account
        
        Args:
            account_id: Account ID to get transfers for
            status: Optional status filter
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List[Transfer]: List of transfer records
        """
        try:
            query = self.db.query(Transfer).filter(Transfer.from_account_id == account_id)
            
            if status:
                query = query.filter(Transfer.status == status)
            
            query = query.order_by(Transfer.created_at.desc())
            query = query.limit(limit).offset(offset)
            
            return query.all()
            
        except Exception:
            return []
    
    def get_transfer_by_id(self, transfer_id: int) -> Optional[Transfer]:
        """
        Get transfer details by ID
        
        Args:
            transfer_id: Transfer ID to retrieve
            
        Returns:
            Optional[Transfer]: Transfer record if found, None otherwise
        """
        try:
            return self.db.query(Transfer).filter(Transfer.id == transfer_id).first()
        except Exception:
            return None
    
    def cancel_transfer(self, transfer_id: int) -> bool:
        """
        Cancel pending transfer
        Implementation will be added in Phase 5 (User Story 3)
        """
        # TODO: Implement in Phase 5
        raise NotImplementedError("Transfer cancellation not implemented yet")
    
    def update_transfer_status(self, transfer_id: int, status: str, 
                             error_message: Optional[str] = None) -> bool:
        """
        Update transfer status and completion timestamp
        
        Args:
            transfer_id: Transfer ID to update
            status: New status value
            error_message: Optional error message for failed transfers
            
        Returns:
            bool: True if update successful, False otherwise
        """
        try:
            transfer = self.db.query(Transfer).filter(Transfer.id == transfer_id).first()
            if not transfer:
                return False
            
            transfer.status = status
            if error_message:
                transfer.error_message = error_message
            
            if status in ["COMPLETED", "FAILED", "CANCELLED"]:
                transfer.completed_at = datetime.now()
            
            self.db.commit()
            return True
            
        except Exception:
            self.db.rollback()
            return False

    def _execute_internal_transfer(self, transfer: Transfer) -> None:
        """
        Execute internal transfer between accounts
        
        Args:
            transfer: Transfer record to execute
            
        Raises:
            RuntimeError: If transfer execution fails
        """
        try:
            transfer.status = "IN_PROGRESS"
            
            # Debit from source account
            if not self._update_account_balance(transfer.from_account_id, transfer.amount, "debit"):
                raise RuntimeError("Failed to debit source account")
            
            # Find destination account and credit
            to_account = self.db.query(Account).filter(
                Account.account_number == transfer.to_account_number
            ).first()
            
            if not to_account:
                # Rollback the debit
                self._update_account_balance(transfer.from_account_id, transfer.amount, "credit")
                raise RuntimeError("Destination account not found")
            
            if not self._update_account_balance(to_account.id, transfer.amount, "credit"):
                # Rollback the debit
                self._update_account_balance(transfer.from_account_id, transfer.amount, "credit")
                raise RuntimeError("Failed to credit destination account")
            
            # Create transaction records
            self._create_transaction_record(transfer)
            
            # Update transfer status to completed
            transfer.status = "COMPLETED"
            transfer.completed_at = datetime.now()
            
        except Exception as e:
            transfer.status = "FAILED"
            transfer.error_message = str(e)
            transfer.completed_at = datetime.now()
            raise
    
    def _generate_reference_number(self) -> str:
        """Generate unique reference number for transfer"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_id = str(uuid.uuid4())[:8].upper()
        return f"TXF{timestamp}{unique_id}"
    
    def _create_transaction_record(self, transfer: Transfer) -> Transaction:
        """
        Create transaction record for completed transfer
        
        Args:
            transfer: Completed transfer record
            
        Returns:
            Transaction: Created transaction record
        """
        try:
            # Get updated account balance
            account = self.db.query(Account).filter(
                Account.id == transfer.from_account_id
            ).first()
            
            if not account:
                raise ValueError("Account not found for transaction record")
            
            # Create transaction record for the sender (withdrawal)
            transaction = Transaction(
                account_id=transfer.from_account_id,
                transaction_type="withdrawal",
                amount=transfer.amount,  # Positive amount with withdrawal type
                description=f"Transfer to {transfer.to_account_number}" + 
                          (f": {transfer.description}" if transfer.description else ""),
                recipient_account=transfer.to_account_number,
                balance_after=account.balance,
                reference_number=self._generate_reference_number(),
                status="completed"
            )
            
            self.db.add(transaction)
            self.db.flush()  # Get transaction ID
            
            # Update transfer with transaction reference
            transfer.transaction_id = transaction.id
            
            # For internal transfers, also create a transaction record for the recipient
            if transfer.transfer_type == "INTERNAL":
                to_account = self.db.query(Account).filter(
                    Account.account_number == transfer.to_account_number
                ).first()
                
                if to_account:
                    recipient_transaction = Transaction(
                        account_id=to_account.id,
                        transaction_type="deposit",
                        amount=transfer.amount,  # Positive for incoming transfer
                        description=f"Transfer from {account.account_number}" + 
                                  (f": {transfer.description}" if transfer.description else ""),
                        recipient_account=account.account_number,
                        balance_after=to_account.balance,
                        reference_number=self._generate_reference_number(),
                        status="completed"
                    )
                    
                    self.db.add(recipient_transaction)
            
            return transaction
            
        except Exception as e:
            raise RuntimeError(f"Failed to create transaction record: {str(e)}")
    
    def _check_account_balance(self, account_id: int, amount: float) -> bool:
        """
        Check if account has sufficient balance for transfer
        
        Args:
            account_id: Account ID to check
            amount: Amount to check against balance
            
        Returns:
            bool: True if sufficient balance, False otherwise
        """
        try:
            account = self.db.query(Account).filter(Account.id == account_id).first()
            if not account:
                return False
            
            # Check if balance is sufficient (including any fees)
            return account.balance >= amount
            
        except Exception:
            return False
    
    def _update_account_balance(self, account_id: int, amount: float, 
                              operation: str) -> bool:
        """
        Update account balance (debit/credit)
        
        Args:
            account_id: Account ID to update
            amount: Amount to add/subtract
            operation: 'debit' to subtract, 'credit' to add
            
        Returns:
            bool: True if update successful, False otherwise
        """
        try:
            account = self.db.query(Account).filter(Account.id == account_id).first()
            if not account:
                return False
            
            if operation == "debit":
                # Check for sufficient balance before debiting
                if account.balance < amount:
                    return False
                account.balance -= amount
            elif operation == "credit":
                account.balance += amount
            else:
                raise ValueError(f"Invalid operation: {operation}")
            
            account.updated_at = datetime.now()
            return True
            
        except Exception:
            return False