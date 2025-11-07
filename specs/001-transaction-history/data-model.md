# 데이터 모델: 입출금 내역 조회

**생성일**: 2025-11-07  
**목적**: 거래 내역 시스템의 데이터 구조 및 관계 정의

## 핵심 엔티티

### Account (계좌)

**목적**: 사용자의 은행 계좌 정보를 관리

**필드**:
- `id` (Integer, Primary Key): 계좌 고유 식별자
- `account_number` (String, 20자, Unique): 계좌번호 (예: "1234-567-890123")
- `account_name` (String, 100자): 계좌 별칭 (예: "메인 통장", "적금 계좌")
- `balance` (Decimal, 정밀도 15,2): 현재 잔액 (원화 기준)
- `created_at` (DateTime): 계좌 생성 일시
- `updated_at` (DateTime): 최종 수정 일시

**검증 규칙**:
- account_number: 숫자와 하이픈만 허용, 고유값
- balance: 음수 허용 (마이너스 통장 가능)
- account_name: 필수 입력, 공백 문자 제거

**관계**:
- `transactions`: 이 계좌의 거래 내역 목록 (One-to-Many)

---

### Transaction (거래)

**목적**: 개별 금융 거래 정보를 저장

**필드**:
- `id` (Integer, Primary Key): 거래 고유 식별자
- `account_id` (Integer, Foreign Key): 연관된 계좌 ID
- `transaction_date` (DateTime): 거래 발생 일시
- `transaction_type` (Enum): 거래 유형
  - `DEPOSIT` - 입금
  - `WITHDRAWAL` - 출금
- `amount` (Decimal, 정밀도 15,2): 거래 금액 (항상 양수)
- `counterpart` (String, 200자): 거래 상대방 (예: "ATM 출금", "월급", "편의점 결제")
- `memo` (String, 500자, Nullable): 거래 메모/설명 (선택사항)
- `balance_after` (Decimal, 정밀도 15,2): 거래 후 잔액
- `reference_number` (String, 50자, Nullable): 거래 참조번호 (은행 내부 번호)
- `created_at` (DateTime): 레코드 생성 일시

**검증 규칙**:
- transaction_date: 미래 날짜 불허용
- amount: 반드시 양수 (0 불허용)
- transaction_type: DEPOSIT 또는 WITHDRAWAL만 허용
- counterpart: 필수 입력, 최소 2자 이상
- memo: 선택사항, HTML 태그 불허용
- balance_after: 계산된 값으로 저장

**관계**:
- `account`: 소속 계좌 정보 (Many-to-One)

**인덱스**:
- `idx_transaction_date`: transaction_date 컬럼 (날짜 범위 조회 최적화)
- `idx_account_date`: (account_id, transaction_date) 복합 인덱스
- `idx_transaction_type`: transaction_type 컬럼 (필터링 최적화)

---

## 데이터 관계도

```
Account (1) ←──── (N) Transaction
│                        │
├── id                   ├── id
├── account_number      ├── account_id (FK)
├── account_name        ├── transaction_date
├── balance             ├── transaction_type
├── created_at          ├── amount
└── updated_at          ├── counterpart
                        ├── memo
                        ├── balance_after
                        ├── reference_number
                        └── created_at
```

## 비즈니스 규칙

### 잔액 계산 규칙

1. **입금 (DEPOSIT)**:
   - `balance_after = previous_balance + amount`
   - 계좌 잔액 증가

2. **출금 (WITHDRAWAL)**:
   - `balance_after = previous_balance - amount`
   - 계좌 잔액 감소
   - 마이너스 잔액 허용 (마이너스 통장)

### 거래 정렬 규칙

- **기본 정렬**: `transaction_date DESC` (최신 거래가 먼저)
- **동일 날짜**: `id DESC` (나중에 생성된 거래가 먼저)

### 데이터 무결성 규칙

1. **참조 무결성**: 
   - 모든 거래는 유효한 계좌에 연결되어야 함
   - 계좌 삭제 시 관련 거래도 함께 삭제 (CASCADE)

2. **데이터 일관성**:
   - 거래 후 잔액은 이전 거래들의 누적 계산과 일치해야 함
   - 거래 금액은 항상 양수여야 함

3. **시간 일관성**:
   - 거래 발생 시간은 계좌 생성 시간 이후여야 함
   - 미래 날짜 거래 생성 불가

## 샘플 데이터 구조

### 계좌 샘플

```json
{
  "id": 1,
  "account_number": "1234-567-890123",
  "account_name": "메인 통장",
  "balance": 1500000.00,
  "created_at": "2024-01-01T09:00:00Z",
  "updated_at": "2024-11-07T14:30:00Z"
}
```

### 거래 샘플

```json
[
  {
    "id": 1,
    "account_id": 1,
    "transaction_date": "2024-11-07T09:30:00Z",
    "transaction_type": "DEPOSIT",
    "amount": 3000000.00,
    "counterpart": "회사 급여",
    "memo": "11월 급여",
    "balance_after": 1500000.00,
    "reference_number": "TXN20241107001",
    "created_at": "2024-11-07T09:30:15Z"
  },
  {
    "id": 2,
    "account_id": 1,
    "transaction_date": "2024-11-06T14:20:00Z",
    "transaction_type": "WITHDRAWAL",
    "amount": 45000.00,
    "counterpart": "온라인 쇼핑몰",
    "memo": "생필품 구매",
    "balance_after": -1500000.00,
    "reference_number": "TXN20241106002",
    "created_at": "2024-11-06T14:20:30Z"
  }
]
```

## 성능 고려사항

### 쿼리 최적화

1. **날짜 범위 조회**: 
   - `transaction_date`에 인덱스 활용
   - WHERE 조건에 BETWEEN 사용

2. **페이지네이션**:
   - LIMIT/OFFSET 대신 커서 기반 페이지네이션 고려
   - 대량 데이터에서 성능 우수

3. **필터링 최적화**:
   - `transaction_type` 인덱스로 유형별 조회 최적화
   - 복합 인덱스로 다중 조건 검색 지원

### 데이터 크기 추정

- **거래 당 평균 크기**: ~200 bytes
- **1년 거래 (월 100건)**: ~240KB
- **10년 데이터**: ~2.4MB
- **SQLite 적합**: 프로토타입 규모에서 충분한 성능

## 마이그레이션 전략

### 초기 스키마

```sql
-- 계좌 테이블
CREATE TABLE accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_number VARCHAR(20) UNIQUE NOT NULL,
    account_name VARCHAR(100) NOT NULL,
    balance DECIMAL(15,2) NOT NULL DEFAULT 0.00,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 거래 테이블
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    transaction_date DATETIME NOT NULL,
    transaction_type VARCHAR(10) NOT NULL CHECK (transaction_type IN ('DEPOSIT', 'WITHDRAWAL')),
    amount DECIMAL(15,2) NOT NULL CHECK (amount > 0),
    counterpart VARCHAR(200) NOT NULL,
    memo VARCHAR(500),
    balance_after DECIMAL(15,2) NOT NULL,
    reference_number VARCHAR(50),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts (id) ON DELETE CASCADE
);

-- 인덱스 생성
CREATE INDEX idx_transaction_date ON transactions(transaction_date);
CREATE INDEX idx_account_date ON transactions(account_id, transaction_date);
CREATE INDEX idx_transaction_type ON transactions(transaction_type);
```

### 샘플 데이터 시드

- 메인 계좌 1개 생성
- 50-100개의 다양한 거래 생성 (최근 6개월)
- 입금/출금 비율: 약 3:7 (현실적인 비율)
- 다양한 거래처 및 금액으로 실제와 유사한 데이터