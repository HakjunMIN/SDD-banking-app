"""
Migration: Create VirtualBank Table
Date: 2025-11-07
Description: Create virtual_banks table for external bank simulation
"""

from sqlalchemy import Column, Integer, String, Text, Boolean
from ...database import Base


def upgrade(engine):
    """Create VirtualBank table"""
    # Import the VirtualBank model
    from ...models.virtual_bank import VirtualBank
    
    # Create the table using SQLAlchemy
    VirtualBank.metadata.create_all(bind=engine)
    print("✅ Created virtual_banks table")


def downgrade(engine):
    """Drop VirtualBank table"""
    from ...models.virtual_bank import VirtualBank
    
    # Drop the table
    VirtualBank.__table__.drop(bind=engine)
    print("✅ Dropped virtual_banks table")


def seed_virtual_banks(db_session):
    """Seed initial virtual bank data"""
    from ...models.virtual_bank import VirtualBank
    
    # Check if data already exists
    if db_session.query(VirtualBank).count() > 0:
        print("Virtual bank data already exists, skipping seed")
        return
    
    virtual_banks = [
        VirtualBank(
            bank_code="KB",
            bank_name="국민은행",
            bank_name_en="Kookmin Bank",
            is_active=True,
            transfer_fee=1000,
            processing_time_min=1,
            processing_time_max=5,
            success_rate=98,
            api_endpoint="https://api.kb.co.kr/v1/transfer",
            description="국민은행 가상 인터페이스"
        ),
        VirtualBank(
            bank_code="SH",
            bank_name="신한은행",
            bank_name_en="Shinhan Bank",
            is_active=True,
            transfer_fee=800,
            processing_time_min=1,
            processing_time_max=3,
            success_rate=99,
            api_endpoint="https://api.shinhan.com/v1/transfer",
            description="신한은행 가상 인터페이스"
        ),
        VirtualBank(
            bank_code="WR",
            bank_name="우리은행",
            bank_name_en="Woori Bank",
            is_active=True,
            transfer_fee=900,
            processing_time_min=2,
            processing_time_max=7,
            success_rate=97,
            api_endpoint="https://api.wooribank.com/v1/transfer",
            description="우리은행 가상 인터페이스"
        ),
        VirtualBank(
            bank_code="HN",
            bank_name="하나은행",
            bank_name_en="Hana Bank",
            is_active=True,
            transfer_fee=1100,
            processing_time_min=1,
            processing_time_max=4,
            success_rate=96,
            api_endpoint="https://api.hanabank.com/v1/transfer",
            description="하나은행 가상 인터페이스"
        ),
        VirtualBank(
            bank_code="IBK",
            bank_name="기업은행",
            bank_name_en="Industrial Bank of Korea",
            is_active=True,
            transfer_fee=750,
            processing_time_min=2,
            processing_time_max=6,
            success_rate=95,
            api_endpoint="https://api.ibk.co.kr/v1/transfer",
            description="기업은행 가상 인터페이스"
        )
    ]
    
    for bank in virtual_banks:
        db_session.add(bank)
    
    db_session.commit()
    print(f"✅ Seeded {len(virtual_banks)} virtual banks")