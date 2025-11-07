# Tasks: 계좌 이체 기능

**Input**: Design documents from `/specs/002-transfer/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: 테스트는 선택적으로 포함됩니다 - 기본 단위/통합 테스트만 포함

**Organization**: 태스크는 사용자 스토리별로 그룹화되어 각 스토리의 독립적 구현과 테스트를 가능하게 합니다.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 병렬 실행 가능 (다른 파일, 종속성 없음)
- **[Story]**: 해당 태스크가 속한 사용자 스토리 (예: US1, US2, US3)
- 설명에 정확한 파일 경로 포함

## 경로 규칙

- **웹 앱**: `backend/src/`, `frontend/src/`
- 아래 경로는 plan.md의 구조를 기반으로 함

---

## Phase 1: 설정 (공유 인프라)

**목적**: 프로젝트 초기화 및 기본 구조

- [x] T001 프로젝트 구조 생성 및 의존성 확인
- [x] T002 [P] 백엔드 새 모델 파일 생성 (transfer.py, virtual_bank.py)
- [x] T003 [P] 프론트엔드 새 컴포넌트 디렉터리 구조 생성
- [x] T004 [P] 새 API 라우터 파일 생성 (backend/src/api/transfer.py)
- [x] T005 [P] 새 서비스 파일 생성 (backend/src/services/transfer_service.py, bank_interface.py)

---

## Phase 2: 기반 구조 (선행 필수)

**목적**: 모든 사용자 스토리 구현 전 완료되어야 하는 핵심 인프라

**⚠️ CRITICAL**: 이 단계 완료 전까지 사용자 스토리 작업 불가

- [ ] T006 데이터베이스 마이그레이션: VirtualBank 테이블 생성 in backend/src/database/migrations/
- [ ] T007 데이터베이스 마이그레이션: Transfer 테이블 생성 in backend/src/database/migrations/
- [ ] T008 데이터베이스 마이그레이션: Account 테이블 이체 한도 필드 추가 in backend/src/database/migrations/
- [ ] T009 데이터베이스 마이그레이션: Transaction 테이블 이체 관련 필드 추가 in backend/src/database/migrations/
- [ ] T010 VirtualBank 모델 구현 in backend/src/models/virtual_bank.py
- [ ] T011 Transfer 모델 구현 in backend/src/models/transfer.py
- [ ] T012 [P] 가상 은행 초기 데이터 생성 스크립트 in backend/src/database/seed_banks.py
- [ ] T013 [P] 입력 검증 유틸리티 구현 (계좌번호, 금액) in backend/src/utils/validators.py
- [ ] T014 [P] Transfer 타입 정의 in frontend/src/types/transfer.ts
- [ ] T015 [P] Transfer API 클라이언트 기본 구조 in frontend/src/services/transferAPI.ts

**Checkpoint**: 기반 구조 완료 - 사용자 스토리 구현이 병렬로 시작 가능

---

## Phase 3: 사용자 스토리 1 - 같은 은행 내 계좌간 이체 (우선순위: P1) 🎯 MVP

**Goal**: 사용자가 내부 계좌로 이체하고 거래 내역에 자동 기록

**Independent Test**: 이체 폼 입력 → 이체 실행 → 거래 내역 확인 (완전한 내부 이체 플로우)

### 백엔드 구현

- [ ] T016 [US1] TransferService 핵심 로직 구현 (내부 이체) in backend/src/services/transfer_service.py
- [ ] T017 [US1] 잔액 검증 로직 구현 in backend/src/services/transfer_service.py
- [ ] T018 [US1] 거래 내역 자동 생성 로직 구현 in backend/src/services/transfer_service.py
- [ ] T019 [US1] Transfer API 엔드포인트 구현 (POST /api/v1/transfers) in backend/src/api/transfer.py
- [ ] T020 [US1] Transfer 내역 조회 API 구현 (GET /api/v1/transfers) in backend/src/api/transfer.py
- [ ] T021 [US1] Transfer 상세 조회 API 구현 (GET /api/v1/transfers/{id}) in backend/src/api/transfer.py

### 프론트엔드 구현

- [ ] T022 [US1] TransferForm 컴포넌트 구현 (내부 이체용) in frontend/src/components/TransferForm.tsx
- [ ] T023 [US1] AccountSelector 컴포넌트 구현 in frontend/src/components/AccountSelector.tsx
- [ ] T024 [US1] Transfer API 클라이언트 구현 (내부 이체) in frontend/src/services/transferAPI.ts
- [ ] T025 [US1] useTransfer 훅 구현 (상태 관리) in frontend/src/hooks/useTransfer.ts
- [ ] T026 [US1] TransferPage 구현 (기본 이체 페이지) in frontend/src/pages/TransferPage.tsx

### 통합 및 테스트

- [ ] T027 [US1] 내부 이체 통합 테스트 in backend/tests/integration/test_transfer_api.py
- [ ] T028 [US1] TransferService 단위 테스트 in backend/tests/unit/test_transfer_service.py
- [ ] T029 [US1] API 라우터에 transfer 엔드포인트 등록 in backend/src/main.py

**MVP 완료**: 기본 내부 이체 기능 동작

---

## Phase 4: 사용자 스토리 2 - 타 은행으로 이체 (가상 인터페이스) (우선순위: P2)

**Goal**: 가상 은행 인터페이스를 통한 타 은행 이체 시뮬레이션

**Independent Test**: 타 은행 선택 → 이체 실행 → 가상 응답 확인 → 거래 내역 기록 확인

### 백엔드 확장

- [ ] T030 [US2] Bank API 엔드포인트 구현 (GET /api/v1/banks) in backend/src/api/transfer.py
- [ ] T031 [US2] 가상 은행 인터페이스 추상 클래스 in backend/src/services/bank_interface.py
- [ ] T032 [US2] 개별 은행 인터페이스 구현 (국민, 신한, 우리, 하나, 기업) in backend/src/services/bank_interface.py
- [ ] T033 [US2] 타 은행 이체 응답 시뮬레이션 로직 in backend/src/services/bank_interface.py
- [ ] T034 [US2] TransferService에 타 은행 이체 로직 추가 in backend/src/services/transfer_service.py
- [ ] T035 [US2] 이체 상태 추적 로직 (PENDING, IN_PROGRESS, COMPLETED, FAILED) in backend/src/services/transfer_service.py

### 프론트엔드 확장

- [ ] T036 [US2] BankSelector 컴포넌트 구현 in frontend/src/components/BankSelector.tsx
- [ ] T037 [US2] TransferForm 컴포넌트 확장 (타 은행 선택 지원) in frontend/src/components/TransferForm.tsx
- [ ] T038 [US2] Bank API 클라이언트 구현 in frontend/src/services/transferAPI.ts
- [ ] T039 [US2] 이체 상태 표시 컴포넌트 in frontend/src/components/TransferStatus.tsx
- [ ] T040 [US2] useTransfer 훅 확장 (타 은행 이체 상태 관리) in frontend/src/hooks/useTransfer.ts

### 통합 및 테스트

- [ ] T041 [US2] 가상 은행 인터페이스 단위 테스트 in backend/tests/unit/test_bank_interface.py
- [ ] T042 [US2] 타 은행 이체 통합 테스트 in backend/tests/integration/test_transfer_api.py
- [ ] T043 [US2] 이체 상태 변경 시나리오 테스트 in backend/tests/unit/test_transfer_service.py

**Phase 2 완료**: 가상 타 은행 이체 기능 동작

---

## Phase 5: 사용자 스토리 3 - 이체 확인 및 취소 기능 (우선순위: P3)

**Goal**: 이체 실행 전 확인 단계 및 취소 기능

**Independent Test**: 이체 정보 입력 → 확인 페이지 → 취소/확인 선택 → 결과 확인

### 백엔드 확장

- [ ] T044 [US3] 이체 검증 API 구현 (POST /api/v1/transfers/validate) in backend/src/api/transfer.py
- [ ] T045 [US3] 계좌 한도 조회 API 구현 (GET /api/v1/account/transfer-limits) in backend/src/api/transfer.py
- [ ] T046 [US3] 이체 상태 조회 API 구현 (GET /api/v1/transfers/{id}/status) in backend/src/api/transfer.py
- [ ] T047 [US3] 이체 사전 검증 로직 in backend/src/services/transfer_service.py
- [ ] T048 [US3] 이체 취소 로직 (PENDING 상태만) in backend/src/services/transfer_service.py

### 프론트엔드 확장

- [ ] T049 [US3] TransferConfirm 컴포넌트 구현 in frontend/src/components/TransferConfirm.tsx
- [ ] T050 [US3] 금액/계좌번호 포맷팅 유틸리티 in frontend/src/utils/formatters.ts
- [ ] T051 [US3] 이체 확인 페이지 라우팅 추가 in frontend/src/pages/TransferConfirmPage.tsx
- [ ] T052 [US3] 이체 검증 API 클라이언트 in frontend/src/services/transferAPI.ts
- [ ] T053 [US3] 다단계 이체 플로우 상태 관리 in frontend/src/hooks/useTransfer.ts

### 통합 및 테스트

- [ ] T054 [US3] 이체 검증 및 취소 테스트 in backend/tests/integration/test_transfer_api.py
- [ ] T055 [US3] 전체 이체 플로우 E2E 테스트 시나리오 in backend/tests/integration/test_transfer_flow.py

**Phase 3 완료**: 완전한 이체 확인/취소 기능

---

## Phase 6: 마무리 및 개선 (통합 및 최적화)

**목적**: 모든 기능 통합, 성능 최적화, 사용자 경험 개선

- [ ] T056 [P] 이체 내역 페이지 기존 거래 내역과 통합 in frontend/src/pages/TransactionHistoryPage.tsx
- [ ] T057 [P] API 오류 처리 및 사용자 친화적 메시지 in frontend/src/utils/errorHandling.ts
- [ ] T058 [P] 이체 로딩 상태 및 진행률 표시 개선 in frontend/src/components/TransferProgress.tsx
- [ ] T059 [P] 전체 애플리케이션 빌드 및 배포 준비
- [ ] T060 [P] 성능 최적화: API 응답 시간 측정 및 개선
- [ ] T061 [P] 전체 기능 통합 테스트 및 버그 수정

---

## Implementation Strategy

### MVP Approach

**Phase 1+2+3 = Minimum Viable Product**
- 내부 계좌간 이체 기능
- 거래 내역 자동 기록
- 기본 유효성 검증

### Incremental Delivery

- **Sprint 1**: Phase 1-3 (내부 이체) → 데모 가능한 MVP
- **Sprint 2**: Phase 4 (타 은행 이체) → 핵심 요구사항 완성
- **Sprint 3**: Phase 5 (확인/취소) → 사용자 경험 완성
- **Sprint 4**: Phase 6 (최적화) → 프로덕션 준비

### Dependencies

**Sequential Dependencies:**
- Phase 1 → Phase 2 → User Stories (순차 실행 필수)
- User Story 1 완료 → User Story 2 시작 (권장)
- User Story 2 완료 → User Story 3 시작

**Parallel Opportunities:**
- Phase 2 완료 후: US1, US2, US3 백엔드/프론트엔드 병렬 개발 가능
- 각 사용자 스토리 내: 백엔드와 프론트엔드 병렬 개발 가능
- 테스트 작성과 구현 병렬 진행 가능 ([P] 태스크들)

### Testing Strategy

**단위 테스트 (선택적)**:
- TransferService 비즈니스 로직
- 각 가상 은행 인터페이스
- 입력 검증 함수

**통합 테스트**:
- 전체 이체 API 플로우
- 데이터베이스 트랜잭션 무결성
- 거래 내역 자동 생성

**E2E 테스트**:
- 완전한 사용자 이체 여정
- 다양한 이체 시나리오 (성공/실패/취소)

---

## Task Summary

**총 태스크 수**: 61개

**사용자 스토리별 태스크 수**:
- Setup/Foundation: 15개 태스크
- User Story 1: 14개 태스크
- User Story 2: 14개 태스크
- User Story 3: 12개 태스크
- Integration/Polish: 6개 태스크

**병렬 실행 가능 태스크**: 34개 ([P] 태그)

**독립 테스트 기준**:
- US1: 내부 이체 → 거래 내역 확인
- US2: 타 은행 이체 → 가상 응답 확인 → 거래 내역 확인
- US3: 이체 확인 → 취소/실행 → 결과 확인

**권장 MVP 범위**: Phase 1-3 (User Story 1)