# Banking App - Speckit 기반 SDD 개발 프로젝트

## 프로젝트 개요

이 뱅킹 앱은 **Speckit 기반 Specification-Driven Development (SDD)** 방식으로 개발된 프로토타입 애플리케이션입니다. 사용자가 거래내역을 조회하고 계좌간 이체를 수행할 수 있는 기본적인 뱅킹 기능을 제공합니다.

## Speckit SDD 개발 방식

이 프로젝트는 명세 기반 개발(SDD) 방법론을 활용하여 체계적으로 구현되었습니다:

### 1. 기능 명세 정의 과정
1. **사용자 요구사항 분석**: 기능별로 브랜치 생성 (`001-transaction-history`, `002-transfer`)
2. **명세서 작성**: `spec.md`에 사용자 스토리와 승인 시나리오 정의
3. **기술 계획**: `plan.md`에 아키텍처와 구현 방향 설계
4. **태스크 분해**: `tasks.md`에 Phase별 구현 태스크 리스트 작성
5. **데이터 모델링**: `data-model.md`에 필요한 데이터 구조 정의

### 2. 단계별 구현
각 기능은 Phase별로 구분되어 체계적으로 개발:
- **Phase 1**: 프로젝트 설정 및 기본 구조
- **Phase 2**: 기반 인프라 (데이터베이스, 모델, 유틸리티)
- **Phase 3**: 사용자 스토리별 핵심 기능 구현
- **Phase 4**: 고급 기능 및 통합 테스트
- **Phase 5**: UI/UX 개선 및 최적화

## Speckit 사용 예시

### 1. 기능 명세서 예시 (`specs/002-transfer/spec.md`)

```markdown
# 기능 명세서: 계좌 이체 기능

**Feature Branch**: `002-transfer`  
**Created**: 2025-11-07  
**Status**: Draft  

## 사용자 시나리오 및 테스트

### 사용자 스토리 1 - 같은 은행 내 계좌간 이체 (우선순위: P1)

사용자가 자신의 계좌에서 같은 은행의 다른 계좌로 이체를 할 수 있습니다. 
수취인 계좌번호, 이체금액, 받는분 성명을 입력하고 이체를 실행합니다. 
이체 완료 후 거래 내역에 출금 기록이 자동으로 추가됩니다.

**승인 시나리오**:
1. **Given** 사용자가 이체 페이지에 접속했을 때, 
   **When** 수취인 계좌번호, 이체금액, 받는분 성명을 입력하고 이체 버튼을 클릭하면, 
   **Then** 이체가 성공적으로 처리되고 확인 메시지가 표시됩니다.

2. **Given** 이체가 완료된 상태에서, 
   **When** 거래 내역 페이지를 확인하면, 
   **Then** 해당 이체 건이 출금 거래로 기록되어 있습니다.
```

### 2. 태스크 리스트 예시 (`specs/002-transfer/tasks.md`)

```markdown
## Phase 3: User Story 1 - 같은 은행 내 계좌간 이체

**목적**: 내부 계좌간 이체 기능 구현

- [x] T016 TransferService 내부 이체 로직 구현 in backend/src/services/transfer_service.py
- [x] T017 Transfer API 엔드포인트 (POST) in backend/src/api/transfer.py  
- [x] T018 Transfer 조회 API 구현 (GET) in backend/src/api/transfer.py
- [x] T019 [P] 이체 검증 로직 구현 in backend/src/services/transfer_service.py
- [x] T020 [P] 트랜잭션 처리 및 계좌 잔액 업데이트 in backend/src/services/transfer_service.py
- [x] T021 [P] 오류 처리 및 예외 상황 대응 in backend/src/api/transfer.py

### Frontend Tasks
- [x] T022 [P] TransferForm 컴포넌트 구현 in frontend/src/components/TransferForm.tsx
- [x] T023 [P] AccountSelector 컴포넌트 구현 in frontend/src/components/AccountSelector.tsx
- [x] T024 [P] useTransfer 훅 구현 in frontend/src/hooks/useTransfer.ts
- [x] T025 TransferPage UI 구현 in frontend/src/pages/TransferPage.tsx
- [x] T026 [P] 이체 성공/실패 처리 in frontend/src/pages/TransferPage.tsx

### Integration Tasks
- [x] T029 라우팅 설정 및 네비게이션 추가 in frontend/src/routes/index.tsx
```

### 3. Speckit 디렉터리 구조 (`specs/`)

```
specs/
├── 001-transaction-history/    # 거래내역 조회 기능
│   ├── spec.md                # 기능 명세서 (사용자 스토리, 승인 시나리오)
│   ├── tasks.md               # 구현 태스크 리스트
│   ├── plan.md                # 기술 계획 및 아키텍처
│   ├── data-model.md          # 데이터 모델 설계
│   ├── quickstart.md          # 빠른 시작 가이드
│   ├── research.md            # 기술 조사 및 참고자료
│   └── contracts/             # API 계약서 디렉터리
└── 002-transfer/              # 계좌이체 기능
    ├── spec.md                # 기능 명세서
    ├── tasks.md               # 구현 태스크 리스트  
    ├── plan.md                # 기술 계획
    ├── data-model.md          # 데이터 모델
    ├── quickstart.md          # 빠른 시작 가이드
    ├── research.md            # 기술 조사
    ├── contracts/             # API 계약서
    └── checklists/            # 체크리스트
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

## Speckit 설치 및 사용법

### Speckit 설치

```bash
npm install -g @speckit/cli
```

또는 프로젝트별로 설치:

```bash
npm install --save-dev @speckit/cli
```

### GitHub Copilot Chat에서 Speckit 사용하기

프로젝트 디렉터리에서 AI assistant를 실행하면 `/speckit.*` 명령어를 사용할 수 있습니다.

#### 1. 프로젝트 원칙 수립

프로젝트의 핵심 원칙과 개발 가이드라인을 설정합니다.

```
/speckit.constitution Create principles focused on code quality, testing standards, user experience consistency, and performance requirements
```

#### 2. 기능 명세 작성

구현하고자 하는 기능을 설명합니다. '무엇을', '왜'에 집중하고, 기술 스택은 나중에 결정합니다.

```
/speckit.specify Build an application that can help me organize my photos in separate photo albums. Albums are grouped by date and can be re-organized by dragging and dropping on the main page. Albums are never in other nested albums. Within each album, photos are previewed in a tile-like interface.
```

#### 3. 기술 구현 계획 생성

기술 스택과 아키텍처 선택사항을 제공합니다.

```
/speckit.plan The application uses Vite with minimal number of libraries. Use vanilla HTML, CSS, and JavaScript as much as possible. Images are not uploaded anywhere and metadata is stored in a local SQLite database.
```

#### 4. 태스크 분해

구현 계획을 실행 가능한 태스크 리스트로 분해합니다.

```
/speckit.tasks
```

#### 5. 구현 실행

계획에 따라 모든 태스크를 실행하고 기능을 구현합니다.

```
/speckit.implement
```

### 실전 사용 예시 - 계좌 이체 기능

#### 1단계: 기능 명세

```
/speckit.specify 사용자가 자신의 계좌에서 다른 계좌로 송금할 수 있는 기능을 만들고 싶습니다. 
수취인 계좌번호, 이체금액, 받는분 성명을 입력받아 이체를 실행합니다.
이체 완료 후 거래내역에 자동으로 기록됩니다.
```

#### 2단계: 기술 계획

```
/speckit.plan Backend는 Python FastAPI와 SQLAlchemy를 사용하고, 
Frontend는 React 18과 TypeScript로 구현합니다.
데이터베이스는 SQLite를 사용하며, 트랜잭션 안전성을 보장합니다.
```

#### 3단계: 태스크 생성 및 구현

```
/speckit.tasks

/speckit.implement
```

### Speckit 명령어 참조

| 명령어 | 설명 |
|--------|------|
| `/speckit.constitution` | 프로젝트 원칙 및 가이드라인 설정 |
| `/speckit.specify` | 기능 명세서 작성 (요구사항 정의) |
| `/speckit.plan` | 기술 구현 계획 수립 |
| `/speckit.tasks` | 실행 가능한 태스크 리스트 생성 |
| `/speckit.implement` | 태스크 기반 구현 실행 |
| `/speckit.verify` | 명세 대비 구현 검증 |

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

이 프로젝트는 Speckit SDD 방식의 실습을 목적으로 합니다. 
