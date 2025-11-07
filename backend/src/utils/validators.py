"""
Validation utilities for banking data
"""

import re
from datetime import datetime
from typing import Union, Optional, Tuple
from decimal import Decimal


class ValidationUtils:
    """Common validation utilities for banking application"""
    
    @staticmethod
    def validate_account_number(account_number: str) -> Tuple[bool, str]:
        """
        Validate Korean bank account number format
        
        Args:
            account_number: Account number to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not account_number:
            return False, "계좌번호가 입력되지 않았습니다."
        
        # Korean bank account format: XXXX-XXXX-XXXX (or similar patterns)
        pattern = r'^\d{4}-\d{4}-\d{4}$'
        
        if not re.match(pattern, account_number):
            return False, "계좌번호는 XXXX-XXXX-XXXX 형식이어야 합니다."
        
        return True, ""
    
    @staticmethod
    def validate_amount(amount: Union[str, int, float, Decimal], min_amount: float = 0) -> Tuple[bool, str]:
        """
        Validate transaction amount
        
        Args:
            amount: Amount to validate
            min_amount: Minimum allowed amount
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            if isinstance(amount, str):
                # Remove currency symbols and commas
                cleaned = amount.replace('원', '').replace(',', '').strip()
                amount_decimal = Decimal(cleaned)
            else:
                amount_decimal = Decimal(str(amount))
            
            if amount_decimal < Decimal(str(min_amount)):
                return False, f"금액은 {min_amount:,.0f}원 이상이어야 합니다."
            
            if amount_decimal > Decimal('999999999999'):  # 1조원 제한
                return False, "금액이 너무 큽니다."
            
            return True, ""
            
        except (ValueError, TypeError):
            return False, "올바른 금액 형식이 아닙니다."
    
    @staticmethod
    def validate_transaction_type(transaction_type: str) -> Tuple[bool, str]:
        """
        Validate transaction type
        
        Args:
            transaction_type: Transaction type to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        valid_types = ["deposit", "withdrawal", "transfer"]
        
        if transaction_type not in valid_types:
            return False, f"거래 유형은 {', '.join(valid_types)} 중 하나여야 합니다."
        
        return True, ""
    
    @staticmethod
    def validate_date_range(start_date: Union[str, datetime], end_date: Union[str, datetime]) -> Tuple[bool, str]:
        """
        Validate date range for queries
        
        Args:
            start_date: Start date
            end_date: End date
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            if isinstance(start_date, str):
                start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            else:
                start_dt = start_date
                
            if isinstance(end_date, str):
                end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            else:
                end_dt = end_date
            
            if start_dt > end_dt:
                return False, "시작 날짜가 종료 날짜보다 늦습니다."
            
            # Check if date range is too large (more than 1 year)
            if (end_dt - start_dt).days > 365:
                return False, "조회 기간은 1년을 초과할 수 없습니다."
            
            return True, ""
            
        except (ValueError, TypeError):
            return False, "올바른 날짜 형식이 아닙니다."


class SecurityUtils:
    """Security-related validation utilities"""
    
    @staticmethod
    def sanitize_input(input_str: str, max_length: int = 255) -> str:
        """
        Sanitize user input to prevent injection attacks
        
        Args:
            input_str: Input string to sanitize
            max_length: Maximum allowed length
            
        Returns:
            Sanitized string
        """
        if not input_str:
            return ""
        
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>"\']', '', input_str)
        
        # Truncate to max length
        sanitized = sanitized[:max_length]
        
        # Remove leading/trailing whitespace
        sanitized = sanitized.strip()
        
        return sanitized
    
    @staticmethod
    def mask_account_number(account_number: str) -> str:
        """
        Mask account number for display (show only last 4 digits)
        
        Args:
            account_number: Account number to mask
            
        Returns:
            Masked account number
        """
        if not account_number or len(account_number) < 4:
            return "****"
        
        return f"****-****-{account_number[-4:]}"
    
    @staticmethod
    def validate_session_token(token: str) -> bool:
        """
        Basic validation for session tokens
        
        Args:
            token: Session token to validate
            
        Returns:
            True if token format is valid
        """
        if not token:
            return False
        
        # Check token format (basic validation)
        return len(token) >= 32 and token.isalnum()


class DataUtils:
    """Data manipulation utilities"""
    
    @staticmethod
    def paginate_results(data: list, page: int, page_size: int) -> dict:
        """
        Paginate data results
        
        Args:
            data: List of data to paginate
            page: Page number (1-based)
            page_size: Number of items per page
            
        Returns:
            Dictionary with paginated data and metadata
        """
        total_items = len(data)
        total_pages = (total_items + page_size - 1) // page_size
        
        if page < 1:
            page = 1
        if page > total_pages and total_pages > 0:
            page = total_pages
        
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        
        paginated_data = data[start_idx:end_idx]
        
        return {
            "data": paginated_data,
            "pagination": {
                "current_page": page,
                "total_pages": total_pages,
                "page_size": page_size,
                "total_items": total_items,
                "has_next": page < total_pages,
                "has_previous": page > 1
            }
        }
    
    @staticmethod
    def sort_transactions(transactions: list, sort_by: str = "date", ascending: bool = False) -> list:
        """
        Sort transaction list by specified field
        
        Args:
            transactions: List of transaction dictionaries
            sort_by: Field to sort by ('date', 'amount', 'description')
            ascending: Sort in ascending order
            
        Returns:
            Sorted transaction list
        """
        if not transactions:
            return []
        
        sort_key_map = {
            "date": lambda x: x.get("transaction_date", ""),
            "amount": lambda x: float(x.get("amount", 0)),
            "description": lambda x: x.get("description", "").lower()
        }
        
        sort_key = sort_key_map.get(sort_by, sort_key_map["date"])
        
        return sorted(transactions, key=sort_key, reverse=not ascending)
    
    @staticmethod
    def filter_transactions(
        transactions: list,
        transaction_type: Optional[str] = None,
        min_amount: Optional[float] = None,
        max_amount: Optional[float] = None,
        description_contains: Optional[str] = None
    ) -> list:
        """
        Filter transactions based on criteria
        
        Args:
            transactions: List of transaction dictionaries
            transaction_type: Filter by transaction type
            min_amount: Minimum amount filter
            max_amount: Maximum amount filter
            description_contains: Filter by description content
            
        Returns:
            Filtered transaction list
        """
        filtered = transactions.copy()
        
        if transaction_type:
            filtered = [t for t in filtered if t.get("transaction_type") == transaction_type]
        
        if min_amount is not None:
            filtered = [t for t in filtered if float(t.get("amount", 0)) >= min_amount]
        
        if max_amount is not None:
            filtered = [t for t in filtered if float(t.get("amount", 0)) <= max_amount]
        
        if description_contains:
            search_term = description_contains.lower()
            filtered = [t for t in filtered if search_term in t.get("description", "").lower()]
        
        return filtered