"""
Migration: Add Transfer Limit Fields to Account Table
Date: 2025-11-07
Description: Add transfer-related fields to existing accounts table
"""

from sqlalchemy import text


def upgrade(engine):
    """Add transfer limit fields to Account table"""
    
    # Add new columns to accounts table
    with engine.connect() as conn:
        try:
            # Add daily transfer limit (default 5,000,000 KRW)
            conn.execute(text(
                "ALTER TABLE accounts ADD COLUMN daily_transfer_limit REAL DEFAULT 5000000.0"
            ))
            print("✅ Added daily_transfer_limit column to accounts table")
            
            # Add per-transaction transfer limit (default 1,000,000 KRW)
            conn.execute(text(
                "ALTER TABLE accounts ADD COLUMN per_transaction_limit REAL DEFAULT 1000000.0"
            ))
            print("✅ Added per_transaction_limit column to accounts table")
            
            # Add account status for transfer eligibility
            conn.execute(text(
                "ALTER TABLE accounts ADD COLUMN transfer_enabled BOOLEAN DEFAULT 1"
            ))
            print("✅ Added transfer_enabled column to accounts table")
            
            # Add last transfer date for daily limit calculation
            conn.execute(text(
                "ALTER TABLE accounts ADD COLUMN last_transfer_date DATE"
            ))
            print("✅ Added last_transfer_date column to accounts table")
            
            # Add daily transfer amount used
            conn.execute(text(
                "ALTER TABLE accounts ADD COLUMN daily_transfer_used REAL DEFAULT 0.0"
            ))
            print("✅ Added daily_transfer_used column to accounts table")
            
            conn.commit()
            
        except Exception as e:
            conn.rollback()
            if "duplicate column name" in str(e).lower():
                print("Transfer limit fields already exist in accounts table")
            else:
                raise e


def downgrade(engine):
    """Remove transfer limit fields from Account table"""
    
    with engine.connect() as conn:
        try:
            # Remove the added columns
            conn.execute(text("ALTER TABLE accounts DROP COLUMN daily_transfer_limit"))
            conn.execute(text("ALTER TABLE accounts DROP COLUMN per_transaction_limit"))
            conn.execute(text("ALTER TABLE accounts DROP COLUMN transfer_enabled"))
            conn.execute(text("ALTER TABLE accounts DROP COLUMN last_transfer_date"))
            conn.execute(text("ALTER TABLE accounts DROP COLUMN daily_transfer_used"))
            
            conn.commit()
            print("✅ Removed transfer limit fields from accounts table")
            
        except Exception as e:
            conn.rollback()
            if "no such column" in str(e).lower():
                print("Transfer limit fields do not exist in accounts table")
            else:
                raise e