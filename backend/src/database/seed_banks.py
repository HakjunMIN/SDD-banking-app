"""
Virtual Bank Data Seeder
Script to populate virtual banks for transfer simulation
"""

from ..database.connection import SessionLocal
from ..models.virtual_bank import VirtualBank


def seed_virtual_banks():
    """Create initial virtual bank data for transfer testing"""
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(VirtualBank).count() > 0:
            print("Virtual bank data already exists!")
            return
        
        print("Creating virtual bank data...")
        
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
                description="국민은행 가상 인터페이스 - 높은 신뢰도"
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
                description="신한은행 가상 인터페이스 - 빠른 처리"
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
                description="우리은행 가상 인터페이스 - 안정적 서비스"
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
                description="하나은행 가상 인터페이스 - 프리미엄 서비스"
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
                description="기업은행 가상 인터페이스 - 경제적 수수료"
            ),
            VirtualBank(
                bank_code="NH",
                bank_name="농협은행",
                bank_name_en="Nonghyup Bank",
                is_active=True,
                transfer_fee=850,
                processing_time_min=2,
                processing_time_max=5,
                success_rate=94,
                api_endpoint="https://api.nonghyup.com/v1/transfer",
                description="농협은행 가상 인터페이스 - 지역 밀착형"
            ),
            VirtualBank(
                bank_code="KEB",
                bank_name="KEB하나은행",
                bank_name_en="KEB Hana Bank",
                is_active=False,  # Merged with Hana
                transfer_fee=1000,
                processing_time_min=3,
                processing_time_max=8,
                success_rate=93,
                api_endpoint="https://api.keb.co.kr/v1/transfer",
                description="KEB하나은행 가상 인터페이스 - 통합 예정"
            )
        ]
        
        for bank in virtual_banks:
            db.add(bank)
        
        db.commit()
        
        active_count = sum(1 for bank in virtual_banks if bank.is_active)
        total_count = len(virtual_banks)
        
        print(f"✅ Successfully created {total_count} virtual banks")
        print(f"   - Active banks: {active_count}")
        print(f"   - Inactive banks: {total_count - active_count}")
        print("Virtual bank codes:", [bank.bank_code for bank in virtual_banks if bank.is_active])
        
    except Exception as e:
        print(f"❌ Error creating virtual bank data: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("🏦 Seeding virtual banks...")
    seed_virtual_banks()
    print("🎉 Virtual bank seeding completed!")