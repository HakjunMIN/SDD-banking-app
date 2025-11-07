# 작업 목록: 입출금 내역 조회

**입력**: `/specs/001-transaction-history/`의 설계 문서
**전제조건**: spec.md (사용자 스토리용 필수)

**테스트**: 명세서에서 명시적으로 요청되지 않았으므로 테스트 작업은 포함하지 않음

**구성**: 작업은 각 스토리의 독립적 구현 및 테스트를 가능하게 하기 위해 사용자 스토리별로 그룹화됨

## 형식: `[ID] [P?] [Story] Description`

- **[P]**: 병렬 실행 가능 (다른 파일, 의존성 없음)
- **[Story]**: 이 작업이 속한 사용자 스토리 (예: US1, US2, US3)
- 설명에 정확한 파일 경로 포함

## 경로 규칙

- **웹 앱**: `backend/src/`, `frontend/src/`
- 사용자 입력에 따라 백엔드는 Python, 프론트엔드는 모던 기술 스택 사용

---

## 1단계: 설정 (공유 인프라)

**목적**: 프로젝트 초기화 및 기본 구조

- [x] T001 백엔드 프로젝트 구조 생성 (backend/src/, backend/pyproject.toml, uv로 설정)
- [x] T002 Python Flask/FastAPI 프로젝트 초기화 in backend/
- [x] T003 [P] SQLite 데이터베이스 설정 in backend/src/database/
- [x] T004 [P] 프론트엔드 프로젝트 구조 생성 (frontend/src/, frontend/package.json)
- [x] T005 [P] React/Next.js 프로젝트 초기화 in frontend/
- [x] T006 [P] 프론트엔드 UI 라이브러리 설정 (Tailwind CSS 또는 MUI) in frontend/

---

## 2단계: 기반 구조 (차단 전제조건)

**목적**: 모든 사용자 스토리가 구현되기 전에 완료되어야 하는 핵심 인프라

**⚠️ 중요**: 이 단계가 완료될 때까지 사용자 스토리 작업을 시작할 수 없음

- [x] T007 SQLite 데이터베이스 스키마 생성 in backend/src/database/schema.sql
- [x] T008 [P] 백엔드 기본 설정 및 환경 변수 관리 in backend/src/config/
- [x] T009 [P] 프론트엔드 기본 라우팅 설정 in frontend/src/routes/
- [x] T010 [P] 백엔드 CORS 및 미들웨어 설정 in backend/src/middleware/
- [x] T011 샘플 거래 데이터 생성 스크립트 in backend/src/data/seed_data.py
- [x] T012 [P] 공통 유틸리티 함수 (날짜 포맷팅, 금액 포맷팅) in backend/src/utils/

**체크포인트**: 기반 구조 준비 완료 - 사용자 스토리 구현을 병렬로 시작 가능

---

## 3단계: 사용자 스토리 1 - 거래 내역 목록 조회 (우선순위: P1) 🎯 MVP ✅ 완료

**목표**: 사용자가 계좌의 거래 내역을 날짜순으로 조회할 수 있는 기능

**독립적 테스트**: 거래 목록 페이지에서 최신 거래부터 시간 역순으로 정렬된 목록 확인

### 사용자 스토리 1 구현

- [x] T013 [P] [US1] Transaction 모델 생성 in backend/src/models/transaction.py
- [x] T014 [P] [US1] Account 모델 생성 in backend/src/models/account.py
- [x] T015 [US1] TransactionService 구현 in backend/src/services/transaction_service.py
- [x] T016 [US1] 거래 내역 조회 API 엔드포인트 in backend/src/routes/transactions.py
- [x] T017 [P] [US1] 프론트엔드 거래 내역 페이지 컴포넌트 in frontend/src/components/TransactionList.jsx
- [x] T018 [P] [US1] 거래 항목 컴포넌트 in frontend/src/components/TransactionItem.jsx
- [x] T019 [US1] API 호출 서비스 구현 in frontend/src/services/transactionApi.js
- [x] T020 [US1] 거래 상세 정보 모달/페이지 in frontend/src/components/TransactionDetail.jsx
- [x] T021 [US1] 금액 및 날짜 포맷팅 유틸리티 in frontend/src/utils/formatters.js
- [x] T022 [US1] 거래 목록 페이지 통합 in frontend/src/pages/TransactionsPage.jsx

**체크포인트**: ✅ 사용자 스토리 1이 완전히 기능하고 독립적으로 테스트 가능 - 완료됨

---

## 4단계: 사용자 스토리 2 - 거래 유형별 필터링 (P2) ✅ 완료

**목표**: 입금/출금/전체 필터링으로 거래 내역을 분류하여 조회

**독립적 테스트**: 필터 버튼 클릭시 해당 유형의 거래만 표시되는지 확인

**의존성**: US1 (거래 목록 조회) 완료 후 시작 가능

- [x] T024 [US2] 거래 유형별 필터링 API 확장 (backend/app/routers/transactions.py - type 쿼리 파라미터)
- [x] T025 [P] [US2] 필터 컨트롤 컴포넌트 (frontend/src/components/TransactionFilter.tsx)
- [x] T026 [US2] 거래 목록에 필터링 기능 통합 (frontend/src/components/TransactionList.tsx 수정)
- [x] T027 [P] [US2] 필터 상태 관리 (frontend/src/hooks/useTransactionFilter.ts)
- [x] T028 [US2] 필터링된 거래 표시 로직 (frontend/src/pages/TransactionsPage.tsx 업데이트)

**체크포인트**: ✅ 사용자 스토리 2가 완전히 기능하고 독립적으로 테스트 가능 - 완료됨

---

## 5단계: 사용자 스토리 3 - 기간별 조회 (P3)

**목표**: 특정 기간의 거래만 조회할 수 있는 날짜 필터링 기능

**독립적 테스트**: 기간 선택시 해당 기간의 거래만 표시되는지 확인

**의존성**: US1 (거래 목록 조회) 완료 후 시작 가능

- [X] T029 [US3] 기간별 조회 API 확장 (backend/app/routers/transactions.py - from_date, to_date 쿼리 파라미터) ✅ 이미 구현됨
- [X] T030 [P] [US3] 날짜 범위 선택 컴포넌트 (frontend/src/components/DateRangeFilter.jsx) ✅ 완료
- [X] T031 [P] [US3] 기간 프리셋 컴포넌트 (frontend/src/components/DatePresets.jsx - 1주일, 1개월, 3개월) ✅ 완료
- [X] T032 [US3] 거래 목록에 날짜 필터링 기능 통합 (frontend/src/components/TransactionList.jsx 수정) ✅ 완료
- [X] T033 [P] [US3] 날짜 유틸리티 함수 (frontend/src/utils/dateUtils.js - 기간 계산 로직) ✅ 완료
- [X] T034 [US3] 날짜 필터링 통합 및 테스트 (frontend/src/pages/TransactionsPage.jsx 업데이트) ✅ 완료

**체크포인트**: ✅ 사용자 스토리 3이 완전히 기능하고 독립적으로 테스트 가능 - 완료됨

---

## 6단계: 통계 및 요약 기능 (추가 기능)

**목적**: 거래 요약 통계 및 대시보드 기능

- [ ] T035 [P] 거래 통계 API 엔드포인트 (backend/app/routers/transactions.py - GET /api/transactions/summary)
- [ ] T036 [P] 계좌 요약 컴포넌트 (frontend/src/components/AccountSummary.jsx)
- [ ] T037 통계 대시보드 페이지 (frontend/src/pages/DashboardPage.jsx)

---

## 7단계: 마무리 및 개선 (횡단 관심사)

**목적**: 코드 품질, 성능, 사용성 개선

- [ ] T038 [P] 백엔드 기본 테스트 작성 (backend/tests/test_transactions.py)
- [ ] T039 [P] 프론트엔드 기본 테스트 작성 (frontend/src/__tests__/TransactionList.test.jsx)
- [ ] T040 [P] API 문서화 및 검증 (OpenAPI 스펙 검토, Swagger UI 확인)
- [ ] T041 [P] 프론트엔드 반응형 디자인 최적화 (모바일 지원)
- [ ] T042 [P] 성능 최적화 (API 응답 시간, 페이지네이션)
- [ ] T043 프로덕션 빌드 및 배포 준비 (Docker 설정, 환경변수 관리)

---

## 의존성 그래프

### 사용자 스토리 완료 순서

```text
설정 (T001-T006) → 기반 구조 (T007-T014)
                                    ↓
                              ✅ US1 (T013-T022) - 완료
                                    ↓
                              ✅ US2 (T024-T028) - 완료
                              └─ US3 (T029-T034)
                                    ↓
                              통계 기능 (T035-T037)
                                    ↓
                              마무리 (T038-T043)
```

### 병렬 실행 예시

**US1 내 병렬화**:
- T015(CRUD) + T019(컴포넌트) + T020(아이템) + T021(모달) + T023(유틸리티)를 병렬 실행
- T016, T017, T018 (API 엔드포인트들)을 T015 완료 후 병렬 실행
- T022 (통합)는 모든 컴포넌트 완료 후 실행

**US2와 US3**:
- US1 완료 후 US2와 US3를 병렬로 개발 가능 (독립적 기능)

---

## 구현 전략

### MVP 범위 (권장)

**1차 목표**: 사용자 스토리 1 (P1) 완료
- 기본적인 거래 내역 조회 및 상세 보기
- 샘플 데이터를 활용한 프로토타입 완성

### 점진적 전달

1. **주차 1**: 설정 + 기반 구조 + US1 (T001-T023)
2. **주차 2**: US2 + US3 (T024-T034)  
3. **주차 3**: 추가 기능 + 마무리 (T035-T043)

### 독립적 테스트 기준

- **US1**: 거래 목록이 표시되고 상세 조회가 가능한지
- **US2**: 필터링이 정확히 작동하는지
- **US3**: 날짜 범위 선택이 올바르게 동작하는지

---

## 형식 검증

✅ **체크리스트 형식**: 모든 작업이 `- [ ] [TaskID] [P?] [Story?] 설명` 형식을 따름  
✅ **작업 ID**: T001부터 T043까지 순차적으로 할당  
✅ **병렬 표시**: [P] 태그가 적절히 표시됨  
✅ **스토리 라벨**: [US1], [US2], [US3] 라벨이 정확히 적용됨  
✅ **파일 경로**: 모든 작업에 구체적인 파일 경로 포함  

**총 작업 수**: 43개  
**사용자 스토리별 작업 수**: US1(9개), US2(5개), US3(6개)  
**병렬 실행 기회**: 23개 작업이 병렬 실행 가능  
**권장 MVP 범위**: US1 (기본 거래 목록 조회)

**독립적 테스트**: 샘플 데이터가 포함된 거래 내역 페이지를 열어서 최신순으로 정렬된 거래 목록이 표시되는지 확인

### 사용자 스토리 1 구현 ✅ 완료

- [x] T013 [P] [US1] Transaction 모델 생성 in backend/src/models/transaction.py
- [x] T014 [P] [US1] Account 모델 생성 in backend/src/models/account.py
- [x] T015 [US1] TransactionService 구현 in backend/src/services/transaction_service.py
- [x] T016 [US1] 거래 내역 조회 API 엔드포인트 in backend/src/routes/transactions.py
- [x] T017 [P] [US1] 프론트엔드 거래 내역 페이지 컴포넌트 in frontend/src/components/TransactionList.tsx
- [x] T018 [P] [US1] 거래 항목 컴포넌트 in frontend/src/components/TransactionItem.tsx
- [x] T019 [US1] API 호출 서비스 구현 in frontend/src/services/api.ts
- [x] T020 [US1] 거래 상세 정보 모달/페이지 in frontend/src/components/TransactionDetail.tsx
- [x] T021 [US1] 금액 및 날짜 포맷팅 유틸리티 in frontend/src/utils/formatters.ts

**체크포인트**: ✅ 사용자 스토리 1이 완전히 기능하고 독립적으로 테스트 가능 - 완료됨

---

## 4단계: 사용자 스토리 2 - 거래 유형별 필터링 (우선순위: P2)

**목표**: 사용자가 입금/출금/전체로 거래 내역을 필터링할 수 있는 기능

**독립적 테스트**: 필터 버튼을 클릭하여 해당 유형의 거래만 표시되는지 확인

### 사용자 스토리 2 구현

- [ ] T022 [US2] TransactionService에 유형별 필터링 로직 추가 in backend/src/services/transaction_service.py
- [ ] T023 [US2] 필터링 지원 API 엔드포인트 업데이트 in backend/src/routes/transactions.py
- [ ] T024 [P] [US2] 필터 버튼 컴포넌트 in frontend/src/components/TransactionFilter.jsx
- [ ] T025 [US2] TransactionList 컴포넌트에 필터링 로직 통합 in frontend/src/components/TransactionList.jsx
- [ ] T026 [US2] 프론트엔드 상태 관리 (필터 상태) in frontend/src/hooks/useTransactionFilter.js

**체크포인트**: 이 시점에서 사용자 스토리 1과 2가 모두 독립적으로 작동해야 함

---

## 5단계: 사용자 스토리 3 - 기간별 조회 (우선순위: P3)

**목표**: 사용자가 특정 기간의 거래 내역만 조회할 수 있는 기능

**독립적 테스트**: 기간 선택 드롭다운을 사용하여 해당 기간의 거래만 표시되는지 확인

### 사용자 스토리 3 구현

- [X] T027 [US3] TransactionService에 기간별 조회 로직 추가 in backend/src/services/transaction_service.py ✅ 이미 구현됨
- [X] T028 [US3] 기간별 조회 지원 API 엔드포인트 업데이트 in backend/src/routes/transactions.py ✅ 이미 구현됨
- [X] T029 [P] [US3] 기간 선택 컴포넌트 in frontend/src/components/DateRangeSelector.jsx ✅ DateRangeFilter.tsx로 완료
- [X] T030 [US3] TransactionList 컴포넌트에 기간 필터링 통합 in frontend/src/components/TransactionList.jsx ✅ 완료
- [X] T031 [US3] 날짜 계산 유틸리티 함수 in frontend/src/utils/dateUtils.js ✅ dateUtils.ts로 완료

**체크포인트**: ✅ 모든 사용자 스토리가 이제 독립적으로 기능함 - 완료됨

---

## 6단계: 개선 및 교차 관심사

**목적**: 마무리 작업 및 성능 최적화

- [ ] T032 [P] 오류 처리 및 로딩 상태 개선 in frontend/src/components/
- [ ] T033 [P] 백엔드 로깅 및 오류 처리 개선 in backend/src/middleware/
- [ ] T034 [P] 반응형 UI 개선 in frontend/src/styles/
- [ ] T035 [P] API 성능 최적화 (페이지네이션 고려) in backend/src/services/
- [ ] T036 [P] 프로덕션 빌드 설정 in frontend/webpack.config.js 또는 package.json
- [ ] T037 [P] 배포용 설정 파일 in docker-compose.yml 또는 deploy/

---

## 의존성 및 실행 순서

### 사용자 스토리 완료 순서
1. **US1 (P1)**: 거래 내역 목록 조회 - MVP 기능
2. **US2 (P2)**: 거래 유형별 필터링 - US1에 의존
3. **US3 (P3)**: 기간별 조회 - US1에 의존

### 병렬 실행 기회
- 각 단계 내에서 [P] 표시된 작업들은 병렬 실행 가능
- 프론트엔드와 백엔드 작업은 API 계약이 정의된 후 병렬 진행 가능
- 각 사용자 스토리는 독립적으로 개발 가능 (US2, US3는 US1 완료 후)

### 구현 전략
- **MVP 우선**: 사용자 스토리 1만으로도 완전한 프로토타입 제공
- **점진적 전달**: 각 사용자 스토리별로 독립적인 가치 제공
- **기술 스택**: Python (Flask/FastAPI) + React/Next.js + SQLite

---

## 요약

**총 작업 수**: 37개
- 설정: 6개
- 기반 구조: 6개  
- 사용자 스토리 1: 9개
- 사용자 스토리 2: 5개
- 사용자 스토리 3: 5개
- 개선: 6개

**사용자 스토리별 작업 수**:
- ✅ US1 (거래 내역 목록): 10개 작업 - 완료
- ✅ US2 (필터링): 5개 작업 - 완료  
- US3 (기간별 조회): 5개 작업

**병렬 실행 기회**: 22개 작업이 병렬 실행 가능 ([P] 표시)

**권장 MVP 범위**: 사용자 스토리 1만으로도 완전한 거래 내역 조회 프로토타입 제공

**형식 검증**: 모든 37개 작업이 체크리스트 형식 (체크박스, ID, 라벨, 파일 경로) 준수