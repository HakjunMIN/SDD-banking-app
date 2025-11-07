"""
Database initialization and sample data
Initialize database with sample data for testing
"""

import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from ..database.connection import SessionLocal
from ..models.database_models import Account, Transaction, TransactionCategory

logger = logging.getLogger(__name__)


def create_sample_data():
    """Create sample data for testing"""
    logger.info("Creating sample data...")
    
    db = SessionLocal()
    try:
        # Check if data already exists
        account_count = db.query(Account).count()
        if account_count > 0:
            logger.info("Sample data already exists, skipping creation")
            return
        
        # Create sample account
        account = Account(
            account_number="1001-2345-6789",
            account_name="김철수 주계좌",
            account_type="checking",
            balance=1500000.0  # 150만원
        )
        db.add(account)
        db.commit()
        db.refresh(account)
        logger.info(f"Created sample account: {account.account_name}")
        
        # Create sample transaction categories
        categories = [
            TransactionCategory(name="일반", description="일반 거래", color="#6B7280"),
            TransactionCategory(name="식비", description="식사 및 음료", color="#10B981"),
            TransactionCategory(name="교통비", description="교통 관련 지출", color="#3B82F6"),
            TransactionCategory(name="쇼핑", description="쇼핑 및 구매", color="#8B5CF6"),
            TransactionCategory(name="급여", description="급여 및 수입", color="#EF4444"),
        ]
        
        for category in categories:
            db.add(category)
        db.commit()
        logger.info(f"Created {len(categories)} transaction categories")
        
        # Create sample transactions
        base_date = datetime.now()
        transactions = []
        
        # Recent deposits
        transactions.extend([
            Transaction(
                account_id=account.id,
                transaction_type="deposit",
                amount=2500000.0,
                description="급여 입금",
                balance_after=2500000.0,
                transaction_date=base_date - timedelta(days=5),
                reference_number="DEP20241107001",
                status="completed"
            ),
            Transaction(
                account_id=account.id,
                transaction_type="deposit",
                amount=50000.0,
                description="이자 지급",
                balance_after=2550000.0,
                transaction_date=base_date - timedelta(days=3),
                reference_number="DEP20241107002",
                status="completed"
            ),
        ])
        
        # Recent withdrawals
        transactions.extend([
            Transaction(
                account_id=account.id,
                transaction_type="withdrawal",
                amount=150000.0,
                description="ATM 출금",
                balance_after=2400000.0,
                transaction_date=base_date - timedelta(days=2),
                reference_number="WTH20241107001",
                status="completed"
            ),
            Transaction(
                account_id=account.id,
                transaction_type="withdrawal",
                amount=80000.0,
                description="마트 결제",
                balance_after=2320000.0,
                transaction_date=base_date - timedelta(days=1),
                reference_number="WTH20241107002",
                status="completed"
            ),
            Transaction(
                account_id=account.id,
                transaction_type="withdrawal",
                amount=820000.0,
                description="월세 이체",
                balance_after=1500000.0,
                transaction_date=base_date,
                reference_number="WTH20241107003",
                status="completed"
            ),
        ])
        
        # Add transfers
        transactions.extend([
            Transaction(
                account_id=account.id,
                transaction_type="transfer",
                amount=100000.0,
                description="용돈 송금",
                recipient_account="9999-8888-7777",
                balance_after=2220000.0,
                transaction_date=base_date - timedelta(days=1, hours=2),
                reference_number="TRF20241107001",
                status="completed"
            ),
        ])
        
        for transaction in transactions:
            db.add(transaction)
        
        db.commit()
        logger.info(f"Created {len(transactions)} sample transactions")
        
        # Update account balance to final balance
        account.balance = 1500000.0  # Final balance after all transactions
        db.commit()
        
        logger.info("Sample data creation completed successfully!")
        
    except Exception as e:
        logger.error(f"Error creating sample data: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    create_sample_data()