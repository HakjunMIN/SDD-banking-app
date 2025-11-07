"""
Common utility functions for date and currency formatting
"""

from datetime import datetime, date
from typing import Optional, Union, Dict
from decimal import Decimal, ROUND_HALF_UP


class DateFormatter:
    """Utility class for date formatting in Korean locale"""
    
    @staticmethod
    def format_date(date_obj: Union[datetime, date], format_type: str = "standard") -> str:
        """
        Format date according to Korean conventions
        
        Args:
            date_obj: Date or datetime object to format
            format_type: Type of formatting
                - "standard": 2024-01-15
                - "korean": 2024년 1월 15일
                - "short": 01/15
                - "full": 2024년 1월 15일 (월요일)
                - "relative": 오늘, 어제, 3일 전
        
        Returns:
            Formatted date string
        """
        if isinstance(date_obj, str):
            try:
                date_obj = datetime.fromisoformat(date_obj.replace('Z', '+00:00'))
            except ValueError:
                return date_obj
        
        if format_type == "standard":
            return date_obj.strftime("%Y-%m-%d")
        
        elif format_type == "korean":
            return date_obj.strftime("%Y년 %m월 %d일")
        
        elif format_type == "short":
            return date_obj.strftime("%m/%d")
        
        elif format_type == "full":
            weekdays = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
            weekday_name = weekdays[date_obj.weekday()]
            return f"{date_obj.strftime('%Y년 %m월 %d일')} ({weekday_name})"
        
        elif format_type == "relative":
            return DateFormatter._format_relative_date(date_obj)
        
        else:
            return date_obj.strftime("%Y-%m-%d")
    
    @staticmethod
    def _format_relative_date(date_obj: Union[datetime, date]) -> str:
        """Format date relative to today"""
        if isinstance(date_obj, datetime):
            target_date = date_obj.date()
        else:
            target_date = date_obj
        
        today = date.today()
        delta = (today - target_date).days
        
        if delta == 0:
            return "오늘"
        elif delta == 1:
            return "어제"
        elif delta == 2:
            return "그제"
        elif delta < 7:
            return f"{delta}일 전"
        elif delta < 30:
            weeks = delta // 7
            return f"{weeks}주 전"
        elif delta < 365:
            months = delta // 30
            return f"{months}개월 전"
        else:
            years = delta // 365
            return f"{years}년 전"
    
    @staticmethod
    def format_time(datetime_obj: datetime, format_type: str = "standard") -> str:
        """
        Format time according to Korean conventions
        
        Args:
            datetime_obj: Datetime object to format
            format_type: Type of formatting
                - "standard": 14:30:15
                - "korean": 오후 2시 30분
                - "short": 14:30
        
        Returns:
            Formatted time string
        """
        if isinstance(datetime_obj, str):
            try:
                datetime_obj = datetime.fromisoformat(datetime_obj.replace('Z', '+00:00'))
            except ValueError:
                return datetime_obj
        
        if format_type == "standard":
            return datetime_obj.strftime("%H:%M:%S")
        
        elif format_type == "korean":
            hour = datetime_obj.hour
            minute = datetime_obj.minute
            
            if hour == 0:
                return f"오전 12시{f' {minute}분' if minute > 0 else ''}"
            elif hour < 12:
                return f"오전 {hour}시{f' {minute}분' if minute > 0 else ''}"
            elif hour == 12:
                return f"오후 12시{f' {minute}분' if minute > 0 else ''}"
            else:
                return f"오후 {hour-12}시{f' {minute}분' if minute > 0 else ''}"
        
        elif format_type == "short":
            return datetime_obj.strftime("%H:%M")
        
        else:
            return datetime_obj.strftime("%H:%M:%S")
    
    @staticmethod
    def format_datetime(datetime_obj: datetime, format_type: str = "standard") -> str:
        """
        Format datetime combining date and time
        
        Args:
            datetime_obj: Datetime object to format
            format_type: Type of formatting
                - "standard": 2024-01-15 14:30:15
                - "korean": 2024년 1월 15일 오후 2시 30분
                - "transaction": 01/15 14:30 (거래내역용)
        
        Returns:
            Formatted datetime string
        """
        if isinstance(datetime_obj, str):
            try:
                datetime_obj = datetime.fromisoformat(datetime_obj.replace('Z', '+00:00'))
            except ValueError:
                return datetime_obj
        
        if format_type == "standard":
            return datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
        
        elif format_type == "korean":
            date_str = DateFormatter.format_date(datetime_obj, "korean")
            time_str = DateFormatter.format_time(datetime_obj, "korean")
            return f"{date_str} {time_str}"
        
        elif format_type == "transaction":
            return datetime_obj.strftime("%m/%d %H:%M")
        
        else:
            return datetime_obj.strftime("%Y-%m-%d %H:%M:%S")


class CurrencyFormatter:
    """Utility class for currency formatting in Korean won"""
    
    @staticmethod
    def format_amount(
        amount: Union[int, float, Decimal, str], 
        format_type: str = "standard",
        show_currency: bool = True
    ) -> str:
        """
        Format monetary amount according to Korean conventions
        
        Args:
            amount: Amount to format
            format_type: Type of formatting
                - "standard": 1,234,567원
                - "compact": 123만원, 12억원
                - "accounting": +1,234,567원 / -1,234,567원
                - "no_decimal": 1,234,567원 (정수로 표시)
            show_currency: Whether to show currency symbol
        
        Returns:
            Formatted amount string
        """
        # Convert to Decimal for precise calculations
        if isinstance(amount, str):
            try:
                amount = Decimal(amount)
            except (ValueError, TypeError):
                return amount
        elif isinstance(amount, (int, float)):
            amount = Decimal(str(amount))
        
        # Round to 2 decimal places
        amount = amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        if format_type == "standard":
            formatted = f"{amount:,.0f}" if amount == int(amount) else f"{amount:,.2f}"
            return f"{formatted}원" if show_currency else formatted
        
        elif format_type == "compact":
            return CurrencyFormatter._format_compact_amount(amount, show_currency)
        
        elif format_type == "accounting":
            if amount >= 0:
                formatted = f"+{amount:,.0f}" if amount == int(amount) else f"+{amount:,.2f}"
            else:
                formatted = f"{amount:,.0f}" if amount == int(amount) else f"{amount:,.2f}"
            return f"{formatted}원" if show_currency else formatted
        
        elif format_type == "no_decimal":
            formatted = f"{int(amount):,}"
            return f"{formatted}원" if show_currency else formatted
        
        else:
            formatted = f"{amount:,.0f}" if amount == int(amount) else f"{amount:,.2f}"
            return f"{formatted}원" if show_currency else formatted
    
    @staticmethod
    def _format_compact_amount(amount: Decimal, show_currency: bool) -> str:
        """Format amount in compact Korean style"""
        abs_amount = abs(amount)
        sign = "-" if amount < 0 else ""
        
        if abs_amount >= 100000000:  # 1억 이상
            value = abs_amount / 100000000
            if value == int(value):
                formatted = f"{sign}{int(value)}억"
            else:
                formatted = f"{sign}{value:.1f}억"
        elif abs_amount >= 10000:  # 1만 이상
            value = abs_amount / 10000
            if value == int(value):
                formatted = f"{sign}{int(value)}만"
            else:
                formatted = f"{sign}{value:.1f}만"
        else:
            formatted = f"{sign}{int(abs_amount):,}"
        
        return f"{formatted}원" if show_currency else formatted
    
    @staticmethod
    def parse_amount(amount_str: str) -> Optional[Decimal]:
        """
        Parse Korean formatted amount string to Decimal
        
        Args:
            amount_str: Formatted amount string (e.g., "1,234,567원", "123만원")
        
        Returns:
            Decimal amount or None if parsing fails
        """
        if not amount_str:
            return None
        
        # Remove currency symbol and spaces
        clean_str = amount_str.replace('원', '').replace(',', '').strip()
        
        try:
            # Handle compact format
            if '억' in clean_str:
                value = float(clean_str.replace('억', '')) * 100000000
                return Decimal(str(value))
            elif '만' in clean_str:
                value = float(clean_str.replace('만', '')) * 10000
                return Decimal(str(value))
            else:
                return Decimal(clean_str)
        except (ValueError, TypeError):
            return None
    
    @staticmethod
    def calculate_percentage_change(
        old_amount: Union[int, float, Decimal],
        new_amount: Union[int, float, Decimal]
    ) -> Decimal:
        """Calculate percentage change between two amounts"""
        old_decimal = Decimal(str(old_amount))
        new_decimal = Decimal(str(new_amount))
        
        if old_decimal == 0:
            return Decimal('0')
        
        change = ((new_decimal - old_decimal) / old_decimal) * 100
        return change.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


class TransactionFormatter:
    """Specialized formatter for banking transactions"""
    
    @staticmethod
    def format_transaction_amount(
        amount: Union[int, float, Decimal],
        transaction_type: str
    ) -> str:
        """Format transaction amount with appropriate sign and styling"""
        formatted_amount = CurrencyFormatter.format_amount(amount, "standard")
        
        if transaction_type == "deposit":
            return f"+{formatted_amount}"
        elif transaction_type in ["withdrawal", "transfer"]:
            return f"-{formatted_amount}"
        else:
            return formatted_amount
    
    @staticmethod
    def format_transaction_description(
        description: str,
        max_length: int = 20
    ) -> str:
        """Format transaction description with length limit"""
        if len(description) <= max_length:
            return description
        else:
            return f"{description[:max_length-3]}..."
    
    @staticmethod
    def format_transaction_summary(
        transaction_date: datetime,
        description: str,
        amount: Union[int, float, Decimal],
        transaction_type: str,
        balance_after: Optional[Union[int, float, Decimal]] = None
    ) -> Dict[str, str]:
        """Format complete transaction summary for display"""
        return {
            "date": DateFormatter.format_datetime(transaction_date, "transaction"),
            "description": TransactionFormatter.format_transaction_description(description),
            "amount": TransactionFormatter.format_transaction_amount(amount, transaction_type),
            "balance": CurrencyFormatter.format_amount(balance_after) if balance_after is not None else "",
            "type_icon": "↑" if transaction_type == "deposit" else "↓" if transaction_type == "withdrawal" else "→"
        }


# Convenience functions for quick formatting
def format_krw(amount: Union[int, float, Decimal, str], compact: bool = False) -> str:
    """Quick function to format Korean won"""
    format_type = "compact" if compact else "standard"
    return CurrencyFormatter.format_amount(amount, format_type)


def format_korean_date(date_obj: Union[datetime, date, str]) -> str:
    """Quick function to format date in Korean"""
    if isinstance(date_obj, str):
        try:
            date_obj = datetime.fromisoformat(date_obj.replace('Z', '+00:00'))
        except (ValueError, TypeError):
            return date_obj
    return DateFormatter.format_date(date_obj, "korean")


def format_relative_date(date_obj: Union[datetime, date, str]) -> str:
    """Quick function to format relative date"""
    if isinstance(date_obj, str):
        try:
            date_obj = datetime.fromisoformat(date_obj.replace('Z', '+00:00'))
        except (ValueError, TypeError):
            return date_obj
    return DateFormatter.format_date(date_obj, "relative")