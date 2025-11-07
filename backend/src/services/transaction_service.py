"""
Transaction Service Layer
Business logic for transaction operations
"""

from typing import List, Optional, Tuple
from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, and_, or_

from ..models.database_models import Transaction, Account
from ..utils.validators import ValidationUtils
from ..utils.formatting import CurrencyFormatter


class TransactionService:
    """Service class for transaction-related business logic"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_transactions(
        self,
        account_id: Optional[int] = None,
        transaction_type: Optional[str] = None,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
        limit: int = 20,
        offset: int = 0,
        sort_by: str = "transaction_date",
        sort_order: str = "desc"
    ) -> Tuple[List[Transaction], int]:
        """
        Get filtered and paginated transactions
        
        Args:
            account_id: Filter by account ID
            transaction_type: Filter by transaction type (deposit, withdrawal, transfer)
            from_date: Start date filter
            to_date: End date filter
            limit: Maximum number of records to return
            offset: Number of records to skip
            sort_by: Field to sort by (transaction_date, amount)
            sort_order: Sort order (asc, desc)
        
        Returns:
            Tuple of (transactions list, total count)
        """
        # Start with base query
        query = self.db.query(Transaction)
        
        # Apply filters
        filters = []
        
        if account_id:
            filters.append(Transaction.account_id == account_id)
        
        if transaction_type:
            # Validate transaction type
            is_valid, error_msg = ValidationUtils.validate_transaction_type(transaction_type)
            if not is_valid:
                raise ValueError(error_msg)
            filters.append(Transaction.transaction_type == transaction_type)
        
        if from_date:
            filters.append(Transaction.transaction_date >= from_date)
        
        if to_date:
            # Add one day to include transactions on the to_date
            to_datetime = datetime.combine(to_date, datetime.max.time())
            filters.append(Transaction.transaction_date <= to_datetime)
        
        # Apply all filters
        if filters:
            query = query.filter(and_(*filters))
        
        # Get total count before pagination
        total_count = query.count()
        
        # Apply sorting
        if sort_by == "transaction_date":
            sort_column = Transaction.transaction_date
        elif sort_by == "amount":
            sort_column = Transaction.amount
        else:
            sort_column = Transaction.transaction_date  # Default
        
        if sort_order.lower() == "asc":
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))
        
        # Apply pagination
        transactions = query.offset(offset).limit(limit).all()
        
        return transactions, total_count
    
    def get_transaction_by_id(self, transaction_id: int) -> Optional[Transaction]:
        """
        Get a specific transaction by ID
        
        Args:
            transaction_id: Transaction ID
        
        Returns:
            Transaction object or None if not found
        """
        return self.db.query(Transaction).filter(Transaction.id == transaction_id).first()
    
    def get_account_summary(self, account_id: int) -> Optional[dict]:
        """
        Get account summary information including balance and recent activity
        
        Args:
            account_id: Account ID
        
        Returns:
            Account summary dict or None if account not found
        """
        account = self.db.query(Account).filter(Account.id == account_id).first()
        
        if not account:
            return None
        
        # Get recent transactions count
        recent_transactions_count = (
            self.db.query(Transaction)
            .filter(Transaction.account_id == account_id)
            .filter(Transaction.transaction_date >= datetime.now().replace(hour=0, minute=0, second=0))
            .count()
        )
        
        # Get total transactions count
        total_transactions = (
            self.db.query(Transaction)
            .filter(Transaction.account_id == account_id)
            .count()
        )
        
        # Calculate monthly summary
        current_month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0)
        
        monthly_deposits = (
            self.db.query(Transaction)
            .filter(and_(
                Transaction.account_id == account_id,
                Transaction.transaction_type == "deposit",
                Transaction.transaction_date >= current_month_start
            ))
            .all()
        )
        
        monthly_withdrawals = (
            self.db.query(Transaction)
            .filter(and_(
                Transaction.account_id == account_id,
                Transaction.transaction_type == "withdrawal",
                Transaction.transaction_date >= current_month_start
            ))
            .all()
        )
        
        monthly_deposit_amount = sum(t.amount for t in monthly_deposits)
        monthly_withdrawal_amount = sum(t.amount for t in monthly_withdrawals)
        
        return {
            "account": {
                "id": account.id,
                "account_number": account.account_number,
                "account_name": account.account_name,
                "account_type": account.account_type,
                "balance": account.balance,
                "formatted_balance": CurrencyFormatter.format_amount(account.balance),
                "created_at": account.created_at,
                "updated_at": account.updated_at
            },
            "summary": {
                "total_transactions": total_transactions,
                "recent_transactions_today": recent_transactions_count,
                "monthly_deposits": {
                    "count": len(monthly_deposits),
                    "amount": monthly_deposit_amount,
                    "formatted_amount": CurrencyFormatter.format_amount(monthly_deposit_amount)
                },
                "monthly_withdrawals": {
                    "count": len(monthly_withdrawals),
                    "amount": monthly_withdrawal_amount,
                    "formatted_amount": CurrencyFormatter.format_amount(monthly_withdrawal_amount)
                },
                "monthly_net": {
                    "amount": monthly_deposit_amount - monthly_withdrawal_amount,
                    "formatted_amount": CurrencyFormatter.format_amount(
                        monthly_deposit_amount - monthly_withdrawal_amount,
                        "accounting"
                    )
                }
            }
        }
    
    def search_transactions(
        self,
        search_term: str,
        account_id: Optional[int] = None,
        limit: int = 20,
        offset: int = 0
    ) -> Tuple[List[Transaction], int]:
        """
        Search transactions by description or recipient account
        
        Args:
            search_term: Search term to look for in description or recipient_account
            account_id: Optional account ID filter
            limit: Maximum number of records to return
            offset: Number of records to skip
        
        Returns:
            Tuple of (transactions list, total count)
        """
        # Sanitize search term
        safe_search_term = ValidationUtils.sanitize_input(search_term)
        
        if not safe_search_term:
            return [], 0
        
        # Build search query
        query = self.db.query(Transaction)
        
        # Apply account filter if provided
        if account_id:
            query = query.filter(Transaction.account_id == account_id)
        
        # Search in description and recipient_account fields
        search_filter = or_(
            Transaction.description.ilike(f"%{safe_search_term}%"),
            Transaction.recipient_account.ilike(f"%{safe_search_term}%")
        )
        
        query = query.filter(search_filter)
        
        # Get total count
        total_count = query.count()
        
        # Order by transaction date (newest first) and apply pagination
        transactions = (
            query.order_by(desc(Transaction.transaction_date))
            .offset(offset)
            .limit(limit)
            .all()
        )
        
        return transactions, total_count
    
    def get_transaction_statistics(
        self,
        account_id: int,
        period_days: int = 30
    ) -> dict:
        """
        Get transaction statistics for specified period
        
        Args:
            account_id: Account ID
            period_days: Number of days to analyze (default: 30)
        
        Returns:
            Dictionary with transaction statistics
        """
        from_date = datetime.now() - timedelta(days=period_days)
        
        transactions = (
            self.db.query(Transaction)
            .filter(and_(
                Transaction.account_id == account_id,
                Transaction.transaction_date >= from_date
            ))
            .all()
        )
        
        deposits = [t for t in transactions if t.transaction_type == "deposit"]
        withdrawals = [t for t in transactions if t.transaction_type == "withdrawal"]
        transfers = [t for t in transactions if t.transaction_type == "transfer"]
        
        total_deposits = sum(t.amount for t in deposits)
        total_withdrawals = sum(t.amount for t in withdrawals)
        total_transfers = sum(t.amount for t in transfers)
        
        avg_deposit = total_deposits / len(deposits) if deposits else 0
        avg_withdrawal = total_withdrawals / len(withdrawals) if withdrawals else 0
        
        return {
            "period_days": period_days,
            "from_date": from_date.isoformat(),
            "to_date": datetime.now().isoformat(),
            "total_transactions": len(transactions),
            "deposits": {
                "count": len(deposits),
                "total_amount": total_deposits,
                "average_amount": avg_deposit,
                "formatted_total": CurrencyFormatter.format_amount(total_deposits),
                "formatted_average": CurrencyFormatter.format_amount(avg_deposit)
            },
            "withdrawals": {
                "count": len(withdrawals),
                "total_amount": total_withdrawals,
                "average_amount": avg_withdrawal,
                "formatted_total": CurrencyFormatter.format_amount(total_withdrawals),
                "formatted_average": CurrencyFormatter.format_amount(avg_withdrawal)
            },
            "transfers": {
                "count": len(transfers),
                "total_amount": total_transfers,
                "formatted_total": CurrencyFormatter.format_amount(total_transfers)
            },
            "net_change": {
                "amount": total_deposits - total_withdrawals - total_transfers,
                "formatted_amount": CurrencyFormatter.format_amount(
                    total_deposits - total_withdrawals - total_transfers,
                    "accounting"
                )
            }
        }


class AccountService:
    """Service class for account-related business logic"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_account_by_id(self, account_id: int) -> Optional[Account]:
        """Get account by ID"""
        return self.db.query(Account).filter(Account.id == account_id).first()
    
    def get_accounts(self, limit: int = 50, offset: int = 0) -> Tuple[List[Account], int]:
        """Get all accounts with pagination"""
        query = self.db.query(Account)
        total_count = query.count()
        
        accounts = (
            query.order_by(Account.created_at)
            .offset(offset)
            .limit(limit)
            .all()
        )
        
        return accounts, total_count