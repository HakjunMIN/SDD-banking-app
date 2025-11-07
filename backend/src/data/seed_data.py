"""
Sample Transaction Data Generation Script
Creates realistic Korean banking sample data for development and testing
"""

import random
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
from pathlib import Path


class SampleDataGenerator:
    """Generate sample banking data for development"""
    
    def __init__(self):
        self.transaction_types = ["deposit", "withdrawal", "transfer"]
        self.categories = [
            {"name": "식비", "description": "식료품 및 외식", "color": "#FF6B6B"},
            {"name": "교통비", "description": "대중교통, 택시, 주유", "color": "#4ECDC4"},
            {"name": "쇼핑", "description": "의류, 생활용품", "color": "#45B7D1"},
            {"name": "의료비", "description": "병원, 약국", "color": "#FFA07A"},
            {"name": "공과금", "description": "전기, 가스, 수도", "color": "#98D8C8"},
            {"name": "급여", "description": "월급, 보너스", "color": "#96CEB4"},
            {"name": "이체", "description": "계좌간 이체", "color": "#FFEAA7"},
            {"name": "투자", "description": "주식, 펀드", "color": "#DDA0DD"},
            {"name": "저축", "description": "적금, 예금", "color": "#B0E0E6"},
            {"name": "기타", "description": "기타 거래", "color": "#D3D3D3"}
        ]
        
        # Korean transaction descriptions by type
        self.transaction_descriptions = {
            "deposit": [
                "월급 입금", "보너스 지급", "이자 입금", "배당금 입금", "환급금 입금",
                "용돈 입금", "판매 수익", "프리랜서 수입", "투자 수익", "캐시백 적립"
            ],
            "withdrawal": [
                "현금 인출", "점심 식사", "저녁 식사", "커피숍", "편의점 구매",
                "마트 장보기", "택시비", "지하철 요금", "버스 요금", "주유비",
                "의료비 결제", "약국 구매", "온라인 쇼핑", "옷 쇼핑", "도서 구매",
                "영화 관람", "헬스장 이용", "미용실", "카페 방문", "배달음식 주문"
            ],
            "transfer": [
                "적금 계좌로 이체", "투자 계좌로 이체", "가족 송금", "친구 송금",
                "공과금 자동이체", "보험료 납부", "대출 상환", "카드 결제대금",
                "월세 이체", "관리비 이체"
            ]
        }
    
    def generate_accounts(self, count: int = 3) -> List[Dict[str, Any]]:
        """Generate sample bank accounts"""
        accounts = []
        account_types = ["checking", "savings", "investment"]
        
        for i in range(count):
            account = {
                "account_number": f"1001-{2000+i:04d}-{3000+i:04d}",
                "account_name": f"{'주거래' if i == 0 else '적금' if i == 1 else '투자'} 계좌",
                "account_type": account_types[i % len(account_types)],
                "balance": random.uniform(50000, 5000000) if i == 0 else random.uniform(100000, 2000000),
                "created_at": (datetime.now() - timedelta(days=random.randint(30, 365))).isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            accounts.append(account)
        
        return accounts
    
    def generate_transactions(self, accounts: List[Dict], count: int = 100) -> List[Dict[str, Any]]:
        """Generate sample transactions for given accounts"""
        transactions = []
        
        for i in range(count):
            account = random.choice(accounts)
            transaction_type = random.choice(self.transaction_types)
            
            # Generate realistic amounts based on transaction type
            if transaction_type == "deposit":
                if random.random() < 0.3:  # 30% chance of salary deposit
                    amount = random.uniform(2500000, 4000000)  # Monthly salary
                else:
                    amount = random.uniform(10000, 500000)
            elif transaction_type == "withdrawal":
                amount = random.uniform(5000, 200000)
            else:  # transfer
                amount = random.uniform(50000, 1000000)
            
            # Random description based on type
            description = random.choice(self.transaction_descriptions[transaction_type])
            
            # Generate transaction date (within last 90 days)
            transaction_date = datetime.now() - timedelta(
                days=random.randint(0, 90),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            
            # Calculate balance after (simplified - in real app this would be calculated properly)
            if transaction_type == "deposit":
                balance_after = account["balance"] + amount
            else:
                balance_after = max(account["balance"] - amount, 0)
            
            transaction = {
                "account_id": 1,  # This will be replaced with actual account ID
                "account_number": account["account_number"],  # Helper field
                "transaction_type": transaction_type,
                "amount": round(amount, 2),
                "description": description,
                "recipient_account": f"2002-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}" if transaction_type == "transfer" else None,
                "transaction_date": transaction_date.isoformat(),
                "balance_after": round(balance_after, 2),
                "reference_number": f"TXN{transaction_date.strftime('%Y%m%d')}{i+1:04d}",
                "status": "completed",
                "created_at": transaction_date.isoformat()
            }
            
            transactions.append(transaction)
        
        # Sort transactions by date (newest first)
        transactions.sort(key=lambda x: x["transaction_date"], reverse=True)
        
        return transactions
    
    def generate_sample_data(self, output_file: str = None) -> Dict[str, Any]:
        """Generate complete sample dataset"""
        accounts = self.generate_accounts(3)
        transactions = self.generate_transactions(accounts, 100)
        
        sample_data = {
            "generated_at": datetime.now().isoformat(),
            "accounts": accounts,
            "transactions": transactions,
            "categories": self.categories,
            "summary": {
                "total_accounts": len(accounts),
                "total_transactions": len(transactions),
                "total_categories": len(self.categories),
                "date_range": {
                    "from": min(t["transaction_date"] for t in transactions),
                    "to": max(t["transaction_date"] for t in transactions)
                }
            }
        }
        
        # Save to file if specified
        if output_file:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(sample_data, f, ensure_ascii=False, indent=2)
            
            print(f"Sample data saved to {output_path}")
        
        return sample_data
    
    def print_summary(self, data: Dict[str, Any]) -> None:
        """Print summary of generated data"""
        print("\n=== 샘플 데이터 생성 완료 ===")
        print(f"생성 시각: {data['generated_at']}")
        print(f"계좌 수: {data['summary']['total_accounts']}")
        print(f"거래 수: {data['summary']['total_transactions']}")
        print(f"카테고리 수: {data['summary']['total_categories']}")
        print(f"기간: {data['summary']['date_range']['from'][:10]} ~ {data['summary']['date_range']['to'][:10]}")
        
        print("\n=== 계좌 목록 ===")
        for account in data['accounts']:
            print(f"- {account['account_number']}: {account['account_name']} ({account['balance']:,.0f}원)")
        
        print("\n=== 최근 거래 (5개) ===")
        for transaction in data['transactions'][:5]:
            amount_str = f"+{transaction['amount']:,.0f}" if transaction['transaction_type'] == 'deposit' else f"-{transaction['amount']:,.0f}"
            print(f"- {transaction['transaction_date'][:10]} | {transaction['description']} | {amount_str}원")


def main():
    """Main function to generate and save sample data"""
    generator = SampleDataGenerator()
    
    # Generate sample data
    data = generator.generate_sample_data(
        output_file="backend/src/data/sample_data.json"
    )
    
    # Print summary
    generator.print_summary(data)


if __name__ == "__main__":
    main()