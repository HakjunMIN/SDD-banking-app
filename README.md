# Banking App - Speckit 기반 SDD 개발 프로젝트

## 프로젝트 개요

이 뱅킹 앱은 **Speckit 기반 Specification-Driven Development (SDD)** 방식으로 개발된 프로토타입 애플리케이션입니다. 사용자가 거래내역을 조회하고 계좌간 이체를 수행할 수 있는 기본적인 뱅킹 기능을 제공합니다.

## 기술 스택

### Backend
- **Python 3.11+** with FastAPI
- **SQLAlchemy** ORM
- **SQLite** 데이터베이스 (프로토타입용)
- **Uvicorn** ASGI 서버

### Frontend  
- **React 18** with TypeScript
- **Tailwind CSS** for styling
- **Vite** build tool
- **Axios** HTTP client

## Speckit SDD 개발 방식

이 프로젝트는 명세 기반 개발(SDD) 방법론을 활용하여 체계적으로 구현되었습니다:

### 1. 기능 명세 정의 (`specs/` 디렉터리)
```
specs/
├── 001-transaction-history/    # 거래내역 조회 기능
│   ├── feature.md             # 기능 상세 명세
│   └── tasks.md              # 구현 태스크 리스트
└── 002-transfer/             # 계좌이체 기능  
    ├── feature.md            # 기능 상세 명세
    └── tasks.md             # 구현 태스크 리스트
```

### 2. 단계별 구현
각 기능은 Phase별로 구분되어 체계적으로 개발:

- **Phase 1**: 기본 인프라 및 API 설정
- **Phase 2**: 거래내역 조회 기능
- **Phase 3**: 내부 계좌간 이체 기능 (현재 완료)
- **Phase 4**: 외부 은행간 이체 기능 (향후 계획)
- **Phase 5**: 이체 확인 및 승인 기능 (향후 계획)

## 현재 구현된 기능

### ✅ 거래내역 조회 (Phase 2)
- 계좌별 거래내역 조회
- 날짜 범위 필터링
- 거래 유형별 필터링
- 페이지네이션 지원

### ✅ 계좌간 이체 (Phase 3)  
- 같은 은행 내 계좌간 실시간 이체
- 잔액 검증 및 한도 확인
- 이체 내역 자동 기록
- 한국어 UI 및 오류 메시지

## Speckit 사용 예시

### 1. 기능 명세서 예시 (`specs/002-transfer/feature.md`)

```markdown
# User Story 1 - 같은 은행 내 계좌간 이체

## 사용자 스토리
고객으로서, 나는 같은 은행의 다른 계좌로 돈을 이체하고 싶다. 

## 수용 조건
1. 출금 계좌를 선택할 수 있어야 함
2. 입금 계좌번호를 입력할 수 있어야 함
3. 이체 금액을 입력할 수 있어야 함
4. 이체 설명을 선택적으로 입력할 수 있어야 함
5. 잔액이 충분한지 확인해야 함
6. 이체가 즉시 처리되어야 함

## 기술적 요구사항
- 실시간 잔액 검증
- 트랜잭션 무결성 보장
- 이체 내역 자동 기록
- 오류 처리 및 사용자 피드백
```

### 2. 태스크 리스트 예시 (`specs/002-transfer/tasks.md`)

```markdown
## Phase 3: User Story 1 - 같은 은행 내 계좌간 이체

### Backend Tasks
- [x] T016: TransferService에 내부 이체 로직 구현
- [x] T017: Transfer API 엔드포인트 생성 (POST /transfers)
- [x] T018: Transfer 조회 API 구현 (GET /transfers)
- [x] T019: 이체 검증 로직 구현
- [x] T020: 트랜잭션 처리 및 계좌 잔액 업데이트
- [x] T021: 오류 처리 및 예외 상황 대응

### Frontend Tasks  
- [x] T022: TransferForm 컴포넌트 구현
- [x] T023: AccountSelector 컴포넌트 구현
- [x] T024: useTransfer 훅 구현
- [x] T025: TransferPage UI 구현
- [x] T026: 이체 성공/실패 처리

### Integration Tasks
- [x] T029: 라우팅 설정 및 네비게이션 추가
```

## 프로젝트 구조

```
banking-app/
├── backend/                 # FastAPI 백엔드
│   ├── src/
│   │   ├── api/            # API 라우터
│   │   ├── models/         # 데이터 모델
│   │   ├── services/       # 비즈니스 로직
│   │   └── database/       # DB 연결 및 설정
│   └── banking_app.db      # SQLite 데이터베이스
├── frontend/               # React 프론트엔드
│   ├── src/
│   │   ├── components/     # React 컴포넌트
│   │   ├── pages/         # 페이지 컴포넌트
│   │   ├── services/      # API 서비스
│   │   └── types/         # TypeScript 타입
└── specs/                 # Speckit 명세서
    ├── 001-transaction-history/
    └── 002-transfer/
```

## 개발 환경 설정

### Backend 실행
```bash
cd backend
uv run uvicorn src.main:app --reload --host 127.0.0.1 --port 8000
```

### Frontend 실행  
```bash
cd frontend
npm install
npm run dev
```

### 테스트용 계좌
- `1001-2345-6789` - 김철수 주계좌 (1,490,000원)
- `1002-3456-7890` - 이영희 적금계좌 (2,010,000원)
- `1003-4567-8901` - 박민수 투자계좌 (5,000,000원)
- `1004-5678-9012` - 최지은 주계좌 (800,000원)

## SDD 방식의 장점

이 프로젝트를 통해 확인할 수 있는 Speckit 기반 SDD의 주요 장점:

1. **체계적인 개발**: 명세 → 태스크 → 구현 단계별 진행
2. **명확한 요구사항**: 사용자 스토리와 수용 조건으로 목표 명확화
3. **추적 가능성**: 각 기능의 구현 상태를 태스크 단위로 관리
4. **협업 효율성**: 개발자와 기획자 간 공통 언어 제공
5. **품질 보증**: 명세 기반 검증으로 요구사항 누락 방지

## 향후 계획

- **Phase 4**: 외부 은행간 이체 기능 구현
- **Phase 5**: 이체 확인 및 승인 프로세스 추가
- **Phase 6**: 모바일 반응형 UI 개선
- **Phase 7**: 보안 강화 및 인증 시스템

## 기여하기

이 프로젝트는 Speckit SDD 방식의 실습을 목적으로 합니다. 새로운 기능 추가 시:

1. `specs/` 디렉터리에 기능 명세서 작성
2. `tasks.md`에 구현 태스크 정의  
3. Phase별로 단계적 구현
4. 각 태스크 완료 시 체크박스 업데이트

---

**개발 방식**: Speckit 기반 SDD (Specification-Driven Development)  
**개발 기간**: 2025년 11월  
**개발자**: AI Assistant & Human Collaboration