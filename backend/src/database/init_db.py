"""
Database Initialization and Sample Data
Script to create tables and populate with sample transaction data
"""

import random
from datetime import datetime, timedelta
from ..database import SessionLocal, create_tables
from ..models.database_models import Account, Transaction, TransactionCategory


def init_database():
    """Initialize database with tables"""
    print("Creating database tables...")
    create_tables()
    print("Database tables created successfully!")


def create_sample_data():
    """Create sample data for testing and demonstration"""
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(Account).count() > 0:
            print("Sample data already exists!")
            return
        
        print("Creating sample data...")
        
        # Create sample accounts
        accounts = [
            Account(
                account_number="1001-2001-3001",
                account_name="메인 체킹 계좌",
                account_type="checking",
                balance=50000.0
            ),
            Account(
                account_number="1001-2001-3002",
                account_name="적금 계좌", 
                account_type="savings",
                balance=150000.0
            )
        ]
        
        for account in accounts:
            db.add(account)
        db.commit()
        
        # Create transaction categories
        categories = [
            TransactionCategory(name="식비", description="식료품 및 외식", color="#FF6B6B"),
            TransactionCategory(name="교통비", description="대중교통, 택시, 주유", color="#4ECDC4"),
            TransactionCategory(name="쇼핑", description="의류, 생활용품", color="#45B7D1"),
            TransactionCategory(name="급여", description="월급, 보너스", color="#96CEB4"),
            TransactionCategory(name="이체", description="계좌간 이체", color="#FFEAA7"),
        ]
        
        for category in categories:
            db.add(category)
        db.commit()
        
        # Create sample transactions
        transaction_data = [
            # Checking account transactions
            ("1001-2001-3001", "deposit", 3000000.0, "월급 입금", None),
            ("1001-2001-3001", "withdrawal", 50000.0, "현금 인출", None),
            ("1001-2001-3001", "withdrawal", 25000.0, "점심 식사", None),
            ("1001-2001-3001", "withdrawal", 15000.0, "지하철 교통카드 충전", None),
            ("1001-2001-3001", "transfer", 100000.0, "적금 계좌로 이체", "1001-2001-3002"),
            ("1001-2001-3001", "withdrawal", 80000.0, "마트 장보기", None),
            ("1001-2001-3001", "withdrawal", 35000.0, "카페 방문", None),
            ("1001-2001-3001", "deposit", 20000.0, "캐시백 적립", None),
            ("1001-2001-3001", "withdrawal", 120000.0, "옷 쇼핑", None),
            ("1001-2001-3001", "withdrawal", 45000.0, "택시비", None),
            
            # Savings account transactions  
            ("1001-2001-3002", "deposit", 100000.0, "체킹 계좌에서 이체", None),
            ("1001-2001-3002", "deposit", 50000.0, "정기 적금", None),
        ]
        
        # Get account objects for balance calculation
        account1 = db.query(Account).filter_by(account_number="1001-2001-3001").first()
        account2 = db.query(Account).filter_by(account_number="1001-2001-3002").first()
        
        current_balance1 = 0.0
        current_balance2 = 0.0
        
        for i, (acc_num, t_type, amount, desc, recipient) in enumerate(transaction_data):
            # Calculate balance after transaction
            if acc_num == "1001-2001-3001":
                if t_type in ["deposit"]:
                    current_balance1 += amount
                else:  # withdrawal, transfer
                    current_balance1 -= amount
                balance_after = current_balance1
                account_id = account1.id
            else:
                current_balance2 += amount
                balance_after = current_balance2  
                account_id = account2.id
            
            # Create transaction
            transaction_date = datetime.now() - timedelta(days=random.randint(1, 30))
            transaction = Transaction(
                account_id=account_id,
                transaction_type=t_type,
                amount=amount,
                description=desc,
                recipient_account=recipient,
                transaction_date=transaction_date,
                balance_after=balance_after,
                reference_number=f"TXN{datetime.now().strftime('%Y%m%d')}{i+1:03d}",
                status="completed"
            )
            db.add(transaction)
        
        # Update account balances
        account1.balance = current_balance1
        account2.balance = current_balance2
        
        db.commit()
        print("Sample data created successfully!")
        print(f"- Created {len(accounts)} accounts")
        print(f"- Created {len(categories)} transaction categories")  
        print(f"- Created {len(transaction_data)} transactions")
        
    except Exception as e:
        db.rollback()
        print(f"Error creating sample data: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_database()
    create_sample_data()