"""
Migration: Create Transfer Table
Date: 2025-11-07
Description: Create transfers table for banking transfers
"""


def upgrade(engine):
    """Create Transfer table"""
    # Import the Transfer model
    from ...models.transfer import Transfer
    
    # Create the table using SQLAlchemy
    Transfer.metadata.create_all(bind=engine)
    print("✅ Created transfers table")


def downgrade(engine):
    """Drop Transfer table"""
    from ...models.transfer import Transfer
    
    # Drop the table
    Transfer.__table__.drop(bind=engine)
    print("✅ Dropped transfers table")