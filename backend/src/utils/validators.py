"""
Validation utilities for banking data
"""

import re
from datetime import datetime
from typing import Union, Optional, Tuple
from decimal import Decimal, InvalidOperation


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


class TransferValidator:
    """Validator class for transfer operations"""
    
    # Korean bank account number patterns
    ACCOUNT_PATTERNS = {
        "KB": r"^\d{3}-\d{6}-\d{2}-\d{3}$|^\d{14}$",  # 국민은행: 14자리 또는 형식
        "SH": r"^\d{3}-\d{2}-\d{6}$|^\d{11}$",       # 신한은행: 11자리 또는 형식
        "WR": r"^\d{4}-\d{3}-\d{6}$|^\d{13}$",       # 우리은행: 13자리 또는 형식
        "HN": r"^\d{3}-\d{6}-\d{5}$|^\d{14}$",       # 하나은행: 14자리 또는 형식
        "IBK": r"^\d{3}-\d{6}-\d{2}-\d{3}$|^\d{14}$", # 기업은행: 14자리 또는 형식
        "NH": r"^\d{3}-\d{4}-\d{4}-\d{2}$|^\d{13}$", # 농협은행: 13자리 또는 형식
        "INTERNAL": r"^\d{10,20}$"  # 내부 계좌: 10-20자리 숫자
    }
    
    # Transfer amount limits
    MIN_TRANSFER_AMOUNT = Decimal('1.00')  # 최소 1원
    MAX_TRANSFER_AMOUNT = Decimal('50000000.00')  # 최대 5천만원 (일반적 한도)
    MAX_DAILY_TRANSFER = Decimal('10000000.00')  # 일일 최대 1천만원
    
    @classmethod
    def validate_account_number_for_transfer(cls, account_number: str, bank_code: Optional[str] = None) -> Tuple[bool, str]:
        """
        계좌번호 형식 검증 (이체용)
        
        Args:
            account_number: 검증할 계좌번호
            bank_code: 은행 코드 (선택적)
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        
        if not account_number:
            return False, "계좌번호는 필수 입력사항입니다."
        
        # 공백 제거
        account_number = account_number.strip().replace(" ", "").replace("-", "")
        
        # 기본 길이 검증
        if len(account_number) < 8 or len(account_number) > 20:
            return False, "계좌번호는 8자리에서 20자리 사이여야 합니다."
        
        # 숫자만 포함되는지 검증
        if not account_number.isdigit():
            return False, "계좌번호는 숫자만 포함해야 합니다."
        
        # 은행별 패턴 검증
        if bank_code and bank_code in cls.ACCOUNT_PATTERNS:
            pattern = cls.ACCOUNT_PATTERNS[bank_code]
            if not re.match(pattern, account_number):
                return False, f"{bank_code} 은행의 계좌번호 형식이 올바르지 않습니다."
        
        return True, ""
    
    @classmethod
    def validate_transfer_amount(cls, amount: float, daily_used: float = 0.0, 
                               account_limit: Optional[float] = None) -> Tuple[bool, str]:
        """
        이체 금액 검증
        
        Args:
            amount: 이체 금액
            daily_used: 오늘 이미 이체한 금액
            account_limit: 계좌별 이체 한도 (선택적)
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        
        if amount is None:
            return False, "이체 금액은 필수 입력사항입니다."
        
        try:
            amount_decimal = Decimal(str(amount))
        except (InvalidOperation, ValueError):
            return False, "올바른 금액을 입력해주세요."
        
        # 최소 금액 검증
        if amount_decimal < cls.MIN_TRANSFER_AMOUNT:
            return False, f"최소 이체 금액은 {cls.MIN_TRANSFER_AMOUNT}원입니다."
        
        # 최대 금액 검증
        if amount_decimal > cls.MAX_TRANSFER_AMOUNT:
            return False, f"최대 이체 금액은 {cls.MAX_TRANSFER_AMOUNT:,}원입니다."
        
        # 일일 한도 검증
        daily_total = Decimal(str(daily_used)) + amount_decimal
        if daily_total > cls.MAX_DAILY_TRANSFER:
            remaining = cls.MAX_DAILY_TRANSFER - Decimal(str(daily_used))
            return False, f"일일 이체 한도를 초과합니다. 남은 한도: {remaining:,}원"
        
        # 계좌별 한도 검증
        if account_limit and amount_decimal > Decimal(str(account_limit)):
            return False, f"계좌별 이체 한도를 초과합니다. 한도: {account_limit:,}원"
        
        return True, ""
    
    @classmethod
    def validate_bank_code(cls, bank_code: str, active_banks: list) -> Tuple[bool, str]:
        """
        은행 코드 검증
        
        Args:
            bank_code: 검증할 은행 코드
            active_banks: 활성화된 은행 코드 목록
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        
        if not bank_code:
            return False, "은행을 선택해주세요."
        
        bank_code = bank_code.upper().strip()
        
        if bank_code not in active_banks:
            return False, "지원하지 않는 은행입니다."
        
        return True, ""
    
    @classmethod
    def validate_transfer_description(cls, description: Optional[str]) -> Tuple[bool, str]:
        """
        이체 설명 검증
        
        Args:
            description: 이체 설명 (선택적)
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        
        if description is None:
            description = ""
        
        description = description.strip()
        
        # 최대 길이 검증
        if len(description) > 100:
            return False, "이체 설명은 100자를 초과할 수 없습니다."
        
        # 특수문자 검증 (선택적)
        forbidden_chars = ['<', '>', '&', '"', "'", '\\']
        if any(char in description for char in forbidden_chars):
            return False, "이체 설명에 사용할 수 없는 문자가 포함되어 있습니다."
        
        return True, ""


def validate_complete_transfer_request(from_account_id: int, to_account_number: str,
                                     amount: float, bank_code: Optional[str] = None,
                                     description: Optional[str] = None,
                                     daily_used: float = 0.0,
                                     account_limit: Optional[float] = None,
                                     active_banks: Optional[list] = None) -> Tuple[bool, str]:
    """
    전체 이체 정보 검증
    
    Args:
        from_account_id: 출금 계좌 ID
        to_account_number: 입금 계좌번호
        amount: 이체 금액
        bank_code: 은행 코드 (외부 이체용)
        description: 이체 설명
        daily_used: 일일 이체 사용량
        account_limit: 계좌 한도
        active_banks: 활성 은행 목록
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    
    # 출금 계좌 검증
    if not from_account_id or from_account_id <= 0:
        return False, "출금 계좌를 선택해주세요."
    
    # 계좌번호 검증
    is_valid, error_msg = TransferValidator.validate_account_number_for_transfer(to_account_number, bank_code)
    if not is_valid:
        return False, error_msg
    
    # 금액 검증
    is_valid, error_msg = TransferValidator.validate_transfer_amount(amount, daily_used, account_limit)
    if not is_valid:
        return False, error_msg
    
    # 은행 코드 검증 (외부 이체인 경우)
    if bank_code:
        if not active_banks:
            active_banks = ["KB", "SH", "WR", "HN", "IBK", "NH"]
        is_valid, error_msg = TransferValidator.validate_bank_code(bank_code, active_banks)
        if not is_valid:
            return False, error_msg
    
    # 설명 검증
    is_valid, error_msg = TransferValidator.validate_transfer_description(description)
    if not is_valid:
        return False, error_msg
    
    return True, "모든 이체 정보가 유효합니다."