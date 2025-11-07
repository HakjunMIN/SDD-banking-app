"""
Migration: Add Transfer-Related Fields to Transaction Table
Date: 2025-11-07
Description: Add transfer-specific fields to existing transactions table
"""

from sqlalchemy import text


def upgrade(engine):
    """Add transfer-related fields to Transaction table"""
    
    with engine.connect() as conn:
        try:
            # Add transfer ID reference for linking to transfers table
            conn.execute(text(
                "ALTER TABLE transactions ADD COLUMN transfer_id INTEGER"
            ))
            print("✅ Added transfer_id column to transactions table")
            
            # Add transfer type to distinguish transfer transactions
            conn.execute(text(
                "ALTER TABLE transactions ADD COLUMN transfer_type VARCHAR(20)"
            ))
            print("✅ Added transfer_type column to transactions table")
            
            # Add bank information for external transfers
            conn.execute(text(
                "ALTER TABLE transactions ADD COLUMN bank_name VARCHAR(100)"
            ))
            print("✅ Added bank_name column to transactions table")
            
            # Add bank code for external transfers
            conn.execute(text(
                "ALTER TABLE transactions ADD COLUMN bank_code VARCHAR(10)"
            ))
            print("✅ Added bank_code column to transactions table")
            
            # Add transfer fee amount
            conn.execute(text(
                "ALTER TABLE transactions ADD COLUMN transfer_fee REAL DEFAULT 0.0"
            ))
            print("✅ Added transfer_fee column to transactions table")
            
            # Add processing time for transfers
            conn.execute(text(
                "ALTER TABLE transactions ADD COLUMN processing_time INTEGER"
            ))
            print("✅ Added processing_time column to transactions table")
            
            # Add error message for failed transfers
            conn.execute(text(
                "ALTER TABLE transactions ADD COLUMN error_message TEXT"
            ))
            print("✅ Added error_message column to transactions table")
            
            # Add external reference number for bank responses
            conn.execute(text(
                "ALTER TABLE transactions ADD COLUMN external_reference VARCHAR(100)"
            ))
            print("✅ Added external_reference column to transactions table")
            
            conn.commit()
            
        except Exception as e:
            conn.rollback()
            if "duplicate column name" in str(e).lower():
                print("Transfer-related fields already exist in transactions table")
            else:
                raise e


def downgrade(engine):
    """Remove transfer-related fields from Transaction table"""
    
    with engine.connect() as conn:
        try:
            # Remove the added columns
            conn.execute(text("ALTER TABLE transactions DROP COLUMN transfer_id"))
            conn.execute(text("ALTER TABLE transactions DROP COLUMN transfer_type"))
            conn.execute(text("ALTER TABLE transactions DROP COLUMN bank_name"))
            conn.execute(text("ALTER TABLE transactions DROP COLUMN bank_code"))
            conn.execute(text("ALTER TABLE transactions DROP COLUMN transfer_fee"))
            conn.execute(text("ALTER TABLE transactions DROP COLUMN processing_time"))
            conn.execute(text("ALTER TABLE transactions DROP COLUMN error_message"))
            conn.execute(text("ALTER TABLE transactions DROP COLUMN external_reference"))
            
            conn.commit()
            print("✅ Removed transfer-related fields from transactions table")
            
        except Exception as e:
            conn.rollback()
            if "no such column" in str(e).lower():
                print("Transfer-related fields do not exist in transactions table")
            else:
                raise e