# 구현 계획: 계좌 이체 기능

**브랜치**: `002-transfer` | **날짜**: 2025-11-07 | **스펙**: [spec.md](./spec.md)
**입력**: `/specs/002-transfer/spec.md`의 기능 명세서

**참고**: 이 템플릿은 `/speckit.plan` 명령으로 작성됩니다.

## 요약

사용자가 다른 계좌로 이체를 실행하고, 가상의 타 은행 인터페이스를 통해 이체를 시뮬레이션할 수 있는 뱅킹 앱 이체 기능을 개발합니다. 이체 완료 후에는 해당 거래가 기존의 거래 내역 시스템에 자동으로 기록됩니다. 기존의 FastAPI + React 아키텍처를 확장하여 이체 서비스와 가상 은행 인터페이스를 추가합니다.

## 기술적 컨텍스트

**Language/Version**: Python 3.11+ (백엔드), TypeScript (프론트엔드)
**Primary Dependencies**: FastAPI, SQLAlchemy, React 18, Tailwind CSS
**Storage**: SQLite (기존 거래 내역과 동일한 데이터베이스)
**Testing**: pytest (백엔드), Jest/Testing Library (프론트엔드)
**Target Platform**: 웹 브라우저 (데스크탑, 모바일 반응형)
**Project Type**: 웹 애플리케이션 (백엔드/프론트엔드 분리)
**Performance Goals**: 이체 처리 < 2초, API 응답 < 500ms, 유효성 검사 < 1초
**Constraints**: 프로토타입 목적으로 실제 은행 연동 없음, 가상 인터페이스 사용
**Scale/Scope**: 내부 계좌간 이체, 가상 타은행 이체, 거래 내역 연동

## 헌장 검사

*게이트: 0단계 연구 전 통과 필수. 1단계 설계 후 재검토.*

### 보안 우선 원칙 검토

**예외 승인됨**: 프로토타입 목적으로 보안 요구사항 완화
- ❌ 다중 인증: 사용자 요청으로 로그인 기능 제외
- ❌ 이체 한도 관리: 프로토타입에서 제외
- ❌ 실시간 사기 탐지: 시뮬레이션 환경에서 제외
- ✅ 잔액 검증: 기본적인 잔액 확인 로직 적용
- ✅ 입력 검증: API 엔드포인트에서 계좌번호, 금액 검증
- ❌ 암호화 통신: 로컬 개발 환경에서는 HTTP 허용

**근거**: 프로토타입 개발 목적으로 가상 은행 인터페이스를 통한 이체 시뮬레이션에 중점을 둡니다.

### 테스트 우선 개발 원칙

**수정 필요**: 명세서에서 테스트 작성을 명시적으로 요청하지 않았으므로 선택적으로 적용
- ✅ 기본 단위 테스트 포함 (이체 로직)
- ✅ API 엔드포인트 통합 테스트
- ✅ 가상 은행 인터페이스 모킹 테스트
- ❌ TDD 전체 적용: 프로토타입 빠른 개발 우선
- ✅ 80% 코드 커버리지 목표

### 모듈형 아키텍처 준수

- ✅ 백엔드/프론트엔드 명확한 분리
- ✅ API 우선 설계 (REST API)
- ✅ 이체 서비스 독립 모듈화
- ✅ 가상 은행 인터페이스 추상화
- ✅ 거래 내역 시스템과의 통합

### 성능 및 신뢰성

- ✅ 이체 처리 시간 < 2초 목표
- ✅ 잔액 부족 오류 처리
- ✅ 계좌번호 유효성 검증
- ✅ 네트워크 오류 시뮬레이션 및 처리
- ✅ 거래 원자성 보장

## 프로젝트 구조

### 문서화 (이 기능)

```text
specs/002-transfer/
├── plan.md              # 이 파일 (/speckit.plan 명령 출력)
├── research.md          # 0단계 출력 (/speckit.plan 명령)
├── data-model.md        # 1단계 출력 (/speckit.plan 명령)
├── quickstart.md        # 1단계 출력 (/speckit.plan 명령)
├── contracts/           # 1단계 출력 (/speckit.plan 명령)
└── tasks.md             # 2단계 출력 (/speckit.tasks 명령 - /speckit.plan에서 생성하지 않음)
```

### 소스 코드 확장 (기존 구조에 추가)

```text
backend/
├── src/
│   ├── models/          # Transfer 모델 추가
│   │   ├── transfer.py  # 이체 거래 엔티티
│   │   └── bank.py      # 가상 은행 정보 엔티티
│   ├── services/        
│   │   ├── transfer_service.py    # 이체 비즈니스 로직
│   │   └── bank_interface.py     # 가상 타 은행 인터페이스
│   ├── api/            
│   │   └── transfer.py  # 이체 API 라우터
│   ├── utils/          
│   │   └── validators.py # 계좌번호, 금액 검증
│   └── config/         
│       └── banks.py    # 가상 은행 설정
├── tests/
│   ├── unit/           
│   │   ├── test_transfer_service.py
│   │   └── test_bank_interface.py
│   └── integration/    
│       └── test_transfer_api.py
└── fixtures/
    └── mock_banks.py   # 가상 은행 테스트 데이터

frontend/
├── src/
│   ├── components/     
│   │   ├── TransferForm.tsx     # 이체 입력 폼
│   │   ├── AccountSelector.tsx  # 계좌 선택
│   │   ├── BankSelector.tsx     # 은행 선택
│   │   └── TransferConfirm.tsx  # 이체 확인
│   ├── pages/         
│   │   └── TransferPage.tsx     # 이체 메인 페이지
│   ├── services/      
│   │   └── transferAPI.ts       # 이체 API 클라이언트
│   ├── utils/         
│   │   └── formatters.ts        # 금액, 계좌번호 포매팅
│   └── hooks/         
│       └── useTransfer.ts       # 이체 상태 관리
└── types/
    └── transfer.ts     # 이체 관련 타입 정의
```

**구조 결정**: 기존의 거래 내역 시스템과 통합되도록 설계했습니다. 이체 기능은 독립적인 모듈로 개발하되, Transfer 모델을 통해 기존의 Transaction 테이블에 이체 완료 기록이 자동으로 저장되도록 합니다.

## 복잡도 추적

> **헌장 검사 위반이 있고 정당화가 필요한 경우에만 작성**

| 위반 | 필요한 이유 | 더 간단한 대안이 거부된 이유 |
|-----------|------------|-------------------------------------|
| 보안 우선 원칙 완화 | 프로토타입 빠른 개발 및 가상 은행 시뮬레이션 | 실제 금융 보안 구현은 개발 복잡도를 10배 증가시킴 |
| 실제 은행 연동 제외 | 사용자가 가짜 인터페이스 명시적 요청 | 실제 은행 API 연동은 프로토타입 범위를 초과 |

## 플래닝 완료 상태

### ✅ 완료된 작업

- [x] **연구 문서** (`research.md`) - 이체 시스템 아키텍처 및 가상 은행 인터페이스 패턴 결정
- [x] **데이터 모델** (`data-model.md`) - Transfer, VirtualBank 엔티티 설계 및 기존 모델과의 관계 정의
- [x] **API 계약** (`contracts/api.yaml`) - OpenAPI 3.0 명세서 작성 (7개 엔드포인트)
- [x] **퀵스타트 가이드** (`quickstart.md`) - 개발 환경 설정 및 실행 방법
- [x] **구현 계획** - 기술 컨텍스트, 프로젝트 구조, 복잡도 추적 완료
- [x] **에이전트 컨텍스트 업데이트** - GitHub Copilot 컨텍스트 파일 업데이트 완료

### 📋 다음 단계

1. **태스크 실행**: `Follow instructions in speckit.tasks.prompt.md` 명령으로 상세 구현 태스크 확인
2. **구현 시작**: 우선순위별 사용자 스토리를 기반으로 단계적 구현

### 🎯 준비된 설계 자료

- **프로젝트 구조**: 백엔드(FastAPI)/프론트엔드(React) 확장 구조 확정
- **데이터베이스**: Transfer, VirtualBank 테이블 추가 설계 완료  
- **API 스펙**: 이체 실행, 내역 조회, 상태 확인, 은행 정보 API 명세 완료
- **개발 환경**: 기존 환경 확장 방법 및 설정 가이드 완료
- **아키텍처**: Event-Driven Transfer Service + Strategy 패턴 은행 인터페이스

**플래닝 단계가 성공적으로 완료되었습니다.** 이제 구현 태스크를 실행할 준비가 되었습니다.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
