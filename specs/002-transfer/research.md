# 연구 보고서: 계좌 이체 기능

**기능**: 계좌 이체 기능  
**브랜치**: `002-transfer`  
**날짜**: 2025-11-07  
**상태**: 완료됨

## 개요

이체 시스템 아키텍처, 가상 은행 인터페이스 패턴, 기존 거래 내역 시스템과의 통합 방안에 대한 연구 결과입니다. 프로토타입 목적으로 실제 은행 API 연동 없이 가상 인터페이스를 통한 이체 시뮬레이션에 중점을 둡니다.

## 아키텍처 패턴 연구

### 이체 시스템 아키텍처

**결정**: Event-Driven Transfer Service 패턴 채택

**근거**: 
- 이체 과정의 여러 단계(검증, 처리, 기록)를 명확히 분리
- 각 단계별 독립적 테스트 가능
- 향후 실제 은행 연동 시 확장 용이

**대안 고려됨**:
- **단순 동기 처리**: 간단하지만 확장성 부족
- **복잡한 Saga 패턴**: 프로토타입에 과도한 복잡도

### 가상 은행 인터페이스 패턴

**결정**: Strategy 패턴 기반 Bank Interface Abstraction

**근거**:
- 각 은행별 특성(응답 시간, 성공률) 독립적 구현
- 새로운 은행 추가 시 기존 코드 수정 없이 확장 가능
- 테스트 시 특정 은행만 모킹 가능

**구현 방식**:
```python
# 추상 인터페이스
class BankInterface(ABC):
    async def transfer_to_bank(self, transfer_request: TransferRequest) -> TransferResult
    
# 구체적 구현
class KBBankInterface(BankInterface): # 국민은행
class ShinhanBankInterface(BankInterface): # 신한은행
```

### 거래 내역 통합 패턴

**결정**: Event Sourcing + Transaction Log 하이브리드

**근거**:
- 기존 Transaction 테이블 구조 활용
- 이체 완료 시 자동으로 거래 내역에 기록
- 이체 상태 추적 및 실패 복구 가능

**통합 방식**:
1. Transfer 엔티티에서 이체 정보 관리
2. 이체 완료 시 Transaction 엔티티 자동 생성
3. 거래 타입으로 "이체출금"/"이체입금" 구분

## 기술 스택 결정

### 백엔드 기술

**FastAPI + SQLAlchemy 확장**:
- **이유**: 기존 프로젝트와 일관성 유지
- **장점**: 기존 개발 환경 그대로 활용 가능
- **확장**: Async 지원으로 은행 인터페이스 호출 효율적 처리

**Pydantic 모델 활용**:
- 이체 요청/응답 데이터 검증
- 은행별 응답 포맷 표준화
- API 문서 자동 생성

### 프론트엔드 기술

**React + TypeScript + Tailwind CSS 확장**:
- **이유**: 기존 거래 내역 페이지와 동일한 기술 스택
- **장점**: 재사용 가능한 컴포넌트 활용
- **추가**: React Hook Form으로 이체 폼 검증

**상태 관리**:
- useState + useEffect로 이체 프로세스 상태 관리
- 기존 거래 내역과 동일한 패턴 유지

## 데이터베이스 설계

### 테이블 구조

**Transfer 테이블**:
- 이체 고유 정보 및 상태 관리
- 기존 Account, Transaction과 연관 관계

**VirtualBank 테이블**:
- 가상 은행 설정 정보
- 응답 시뮬레이션 파라미터

### 관계 설계

```sql
Transfer 1:1 Transaction (이체 완료 시)
Transfer N:1 Account (송금 계좌)
Transfer N:1 VirtualBank (수취 은행)
```

## 보안 고려사항

### 프로토타입 보안

**적용 항목**:
- 입력 검증: 계좌번호 형식, 금액 범위
- 잔액 확인: 송금 가능 금액 검증
- 거래 원자성: DB 트랜잭션으로 데이터 무결성 보장

**제외 항목** (프로토타입):
- 다중 인증, 이체 한도 관리, 실시간 사기 탐지

### 향후 보안 확장

- JWT 토큰 기반 인증 구조 준비
- 이체 한도 관리 인터페이스 설계
- 암호화 통신 준비 (HTTPS 설정)

## 성능 최적화

### 응답 시간 목표

- **이체 처리**: < 2초
- **API 응답**: < 500ms
- **유효성 검사**: < 1초

### 최적화 방안

**가상 은행 인터페이스**:
- 비동기 처리로 병렬 호출
- 응답 캐싱으로 반복 호출 최적화
- 타임아웃 설정으로 무한 대기 방지

**데이터베이스**:
- 인덱스 최적화 (계좌번호, 이체일시)
- 커넥션 풀 설정
- 트랜잭션 범위 최소화

## 테스트 전략

### 단위 테스트

- Transfer Service 비즈니스 로직
- 각 가상 은행 인터페이스
- 유효성 검증 함수

### 통합 테스트

- 이체 API 엔드포인트
- 데이터베이스 연동
- 거래 내역 자동 기록

### 시나리오 테스트

- 성공적인 내부 이체
- 가상 타은행 이체 시뮬레이션
- 잔액 부족, 계좌 오류 등 실패 케이스

## 모니터링 및 로깅

### 로그 설계

```python
# 이체 시작
logger.info("Transfer initiated", extra={
    "transfer_id": transfer.id,
    "from_account": transfer.from_account,
    "amount": transfer.amount
})

# 은행 인터페이스 호출
logger.info("Bank interface called", extra={
    "bank": bank.name,
    "response_time": response_time
})
```

### 메트릭 수집

- 이체 성공/실패율
- 은행별 응답 시간
- API 엔드포인트 성능

## 결론

**핵심 결정사항**:
1. Event-Driven Transfer Service 아키텍처
2. Strategy 패턴 기반 가상 은행 인터페이스
3. 기존 거래 내역 시스템과의 자연스러운 통합
4. FastAPI + React 기술 스택 확장

**다음 단계**: Phase 1 설계에서 상세한 데이터 모델과 API 계약 정의

**리스크**: 없음 (프로토타입 범위에서 관리 가능한 복잡도)