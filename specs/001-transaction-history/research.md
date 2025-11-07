# 연구 문서: 입출금 내역 조회

**생성일**: 2025-11-07  
**목적**: 기술적 불명확성 해결 및 구현 방향 결정

## 기술 스택 연구

### 백엔드 프레임워크 선택

**결정**: FastAPI + uv  
**근거**: 
- Python 3.11+ 지원으로 최신 타입 힌팅 활용
- 자동 OpenAPI 문서 생성으로 API 설계 용이
- 비동기 지원으로 성능 우수
- SQLAlchemy 통합이 원활
- 프로토타입 개발 속도가 빠름
- uv: 빠른 패키지 관리, pip보다 10-100배 빠른 설치 속도

**검토된 대안**:
- Flask: 더 가벼우나 비동기 지원 제한적
- Django: 너무 무거움, 프로토타입에 과도한 기능
- FastAPI 선택으로 개발 속도와 성능의 균형 달성

### 프론트엔드 프레임워크 선택

**결정**: React 18 + Vite + Tailwind CSS  
**근거**: 
- React 18: 최신 모던 프레임워크, 대규모 커뮤니티
- Vite: 빠른 개발 서버, HMR 지원으로 개발 속도 향상
- Tailwind CSS: 유틸리티 퍼스트로 빠른 UI 개발
- TypeScript 옵션으로 타입 안전성 확보 가능

**검토된 대안**:
- Next.js: SSR 불필요 (SPA로 충분)
- Vue.js: React만큼 성숙하지 않은 생태계
- Svelte: 상대적으로 작은 커뮤니티

### 데이터베이스 설계

**결정**: SQLite + SQLAlchemy ORM  
**근거**:
- 프로토타입에 적합한 경량 데이터베이스
- 별도 서버 설치 불필요로 설정 간소화
- SQLAlchemy ORM으로 Python 객체 매핑 용이
- 필요시 PostgreSQL로 쉽게 마이그레이션 가능

**스키마 설계 원칙**:
- 정규화된 테이블 구조
- 외래키 제약조건 사용
- 인덱스를 통한 조회 성능 최적화
- 샘플 데이터 시드 스크립트 포함

## 아키텍처 패턴

### API 설계 패턴

**결정**: RESTful API with OpenAPI  
**근거**:
- 표준화된 HTTP 메서드 사용 (GET, POST, PUT, DELETE)
- 리소스 기반 URL 구조 (/api/transactions)
- JSON 응답 형식으로 프론트엔드 연동 용이
- FastAPI 자동 문서화 활용

**엔드포인트 구조**:
```
GET /api/transactions - 거래 내역 목록 조회
GET /api/transactions/{id} - 특정 거래 상세 조회
GET /api/transactions?type=deposit - 유형별 필터링
GET /api/transactions?from=2024-01-01&to=2024-12-31 - 기간별 조회
```

### 프론트엔드 아키텍처

**결정**: 컴포넌트 기반 아키텍처  
**근거**:
- 재사용 가능한 UI 컴포넌트
- 관심사 분리 (UI, 비즈니스 로직, API 통신)
- React Hook을 통한 상태 관리
- 커스텀 훅으로 로직 재사용

**컴포넌트 계층 구조**:
```
App
├── TransactionList (거래 내역 목록)
├── TransactionItem (개별 거래 항목)
├── TransactionFilter (필터링 컨트롤)
├── DateRangeSelector (기간 선택)
└── TransactionDetail (거래 상세)
```

## 성능 최적화 전략

### 백엔드 최적화

**데이터베이스 최적화**:
- transaction_date 컬럼에 인덱스 생성
- 복합 인덱스 (account_id, transaction_date) 생성
- LIMIT/OFFSET를 통한 페이지네이션 구현

**API 최적화**:
- 응답 데이터 압축 (gzip)
- 적절한 HTTP 캐싱 헤더 설정
- 필요 필드만 선택하는 쿼리 최적화

### 프론트엔드 최적화

**렌더링 최적화**:
- React.memo를 통한 불필요한 재렌더링 방지
- 가상 스크롤링 (많은 거래 내역 처리)
- 디바운싱을 통한 필터링 최적화

**번들 최적화**:
- 코드 스플리팅으로 초기 로딩 시간 단축
- Tree shaking으로 불필요한 코드 제거
- 이미지 및 자산 최적화

## 개발 환경 설정

### 백엔드 개발 환경

**필수 도구**:
- Python 3.11+
- uv (패키지 관리 및 프로젝트 관리)
- pytest (테스팅)
- black, isort (코드 포맷팅)
- flake8 (린팅)

**개발 서버 설정**:
- uvicorn으로 ASGI 서버 실행
- 자동 리로드 활성화
- CORS 설정으로 프론트엔드 연동

### 프론트엔드 개발 환경

**필수 도구**:
- Node.js 18+
- npm 또는 yarn (패키지 관리)
- Vite (개발 서버)
- ESLint, Prettier (코드 품질)
- Jest, Testing Library (테스팅)

**개발 설정**:
- HMR(Hot Module Replacement) 활성화
- 프록시 설정으로 백엔드 API 연동
- 환경 변수를 통한 설정 관리

## 보안 고려사항 (프로토타입용)

### 기본 보안 조치

**적용할 보안 조치**:
- CORS 정책 설정
- 기본적인 입력 검증 (SQL Injection 방지)
- XSS 방지를 위한 출력 이스케이프
- 적절한 HTTP 헤더 설정

**프로토타입으로 제외되는 보안 요소**:
- 사용자 인증/인가
- 데이터 암호화
- 세션 관리
- 감사 로그

## 테스트 전략

### 백엔드 테스트

**단위 테스트**:
- 모델 및 서비스 로직 테스트
- pytest-asyncio를 통한 비동기 테스트
- 목 객체를 통한 데이터베이스 격리

**통합 테스트**:
- API 엔드포인트 전체 흐름 테스트
- 실제 SQLite 데이터베이스 사용
- 테스트 데이터 픽스처 활용

### 프론트엔드 테스트

**컴포넌트 테스트**:
- React Testing Library 사용
- 사용자 상호작용 시나리오 테스트
- API 모킹을 통한 격리된 테스트

**E2E 테스트** (선택사항):
- 주요 사용자 플로우 테스트
- 실제 브라우저 환경에서의 동작 검증

## 배포 전략

### 개발 환경

**로컬 개발**:
- Docker Compose로 전체 스택 구성
- 백엔드: localhost:8000
- 프론트엔드: localhost:3000
- 자동 리로드 및 디버깅 지원

### 프로덕션 준비 (선택사항)

**간단한 배포 옵션**:
- Vercel/Netlify (프론트엔드)
- Heroku/Railway (백엔드)
- 또는 단일 서버에 Docker로 배포

**최적화 고려사항**:
- 정적 파일 CDN 연동
- 데이터베이스 백업 전략
- 모니터링 및 로깅 설정