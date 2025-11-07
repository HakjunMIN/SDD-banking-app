# 빠른 시작: 계좌 이체 기능

**기능**: 계좌 이체 기능  
**브랜치**: `002-transfer`  
**날짜**: 2025-11-07

## 개요

이 가이드는 계좌 이체 기능 개발 환경을 설정하고 기본적인 개발 워크플로우를 안내합니다.

## 사전 준비

### 필수 요구사항

- **기존 프로젝트**: 거래 내역 조회 기능이 구현된 뱅킹 앱
- **Python**: 3.11 이상
- **Node.js**: 18 이상
- **SQLite**: 3.x (기존 데이터베이스 활용)

### 개발 도구

- **IDE**: VS Code (권장)
- **API 테스트**: Postman 또는 Thunder Client
- **데이터베이스**: SQLite Browser (선택사항)

## 환경 설정

### 1. 브랜치 체크아웃

```bash
# 이체 기능 브랜치로 전환
git checkout 002-transfer

# 최신 변경사항 확인
git status
```

### 2. 백엔드 환경 설정

```bash
# 백엔드 디렉터리로 이동
cd backend

# 가상환경 활성화 (이미 설정된 경우)
source venv/bin/activate  # Unix/macOS
# 또는
venv\Scripts\activate     # Windows

# 필요한 패키지 설치 (새로운 의존성이 있을 경우)
pip install -r requirements.txt
```

### 3. 프론트엔드 환경 설정

```bash
# 프론트엔드 디렉터리로 이동
cd frontend

# 의존성 설치 (새로운 패키지가 있을 경우)
npm install
```

### 4. 데이터베이스 마이그레이션

```bash
# 백엔드 디렉터리에서 실행
cd backend

# 이체 기능을 위한 새 테이블 생성
# (마이그레이션 스크립트가 준비되면 실행)
python -m src.database.migrations.create_transfer_tables
```

## 개발 서버 실행

### 백엔드 서버

```bash
# 터미널 1: 백엔드 디렉터리에서
cd backend
uvicorn src.main:app --reload --host 127.0.0.1 --port 8000
```

서버가 실행되면 다음 URL에서 확인 가능:
- **API 문서**: http://localhost:8000/docs
- **건강 상태**: http://localhost:8000/health

### 프론트엔드 서버

```bash
# 터미널 2: 프론트엔드 디렉터리에서
cd frontend
npm run dev
```

개발 서버가 실행되면 다음 URL에서 확인 가능:
- **웹 앱**: http://localhost:3000
- **이체 페이지**: http://localhost:3000/transfer (구현 후)

## API 엔드포인트 확인

### 이체 API 테스트

기본적인 API 엔드포인트를 Postman으로 테스트할 수 있습니다.

**1. 은행 목록 조회**
```http
GET http://localhost:8000/api/v1/banks
Accept: application/json
```

**2. 이체 실행**
```http
POST http://localhost:8000/api/v1/transfers
Content-Type: application/json

{
  "to_account_number": "1234567890123456",
  "to_bank_id": "은행ID",
  "recipient_name": "홍길동",
  "amount": 50000.00,
  "memo": "용돈"
}
```

**3. 이체 내역 조회**
```http
GET http://localhost:8000/api/v1/transfers
Accept: application/json
```

### 예상 응답

```json
{
  "transfer_id": "uuid",
  "status": "PENDING",
  "amount": 50000.00,
  "fee": 500.00,
  "estimated_completion_time": "2025-11-07T15:30:00Z",
  "message": "이체가 정상적으로 접수되었습니다."
}
```

## 개발 워크플로우

### 1. TDD 접근법

```bash
# 새로운 기능 개발 시
# 1단계: 테스트 작성
cd backend/tests
touch unit/test_transfer_service.py

# 2단계: 테스트 실행 (실패 확인)
pytest tests/unit/test_transfer_service.py

# 3단계: 구현 코드 작성
cd ../src/services
touch transfer_service.py

# 4단계: 테스트 통과 확인
pytest tests/unit/test_transfer_service.py
```

### 2. API 우선 개발

1. **API 스키마 확인**: `specs/002-transfer/contracts/api.yaml`
2. **모델 정의**: `backend/src/models/transfer.py`
3. **서비스 구현**: `backend/src/services/transfer_service.py`
4. **라우터 구현**: `backend/src/api/transfer.py`
5. **프론트엔드 연동**: `frontend/src/services/transferAPI.ts`

### 3. 컴포넌트 개발

```bash
# 프론트엔드 컴포넌트 개발 순서
cd frontend/src/components

# 1. 기본 폼 컴포넌트
touch TransferForm.tsx

# 2. 은행 선택 컴포넌트
touch BankSelector.tsx

# 3. 계좌 선택 컴포넌트
touch AccountSelector.tsx

# 4. 확인 화면 컴포넌트
touch TransferConfirm.tsx

# 스타일링 확인
npm run dev
```

## 디버깅 가이드

### 백엔드 디버깅

**로그 확인**:
```bash
# 개발 서버 로그 확인
tail -f backend/logs/app.log
```

**데이터베이스 확인**:
```bash
# SQLite 데이터베이스 연결
cd database
sqlite3 bankingapp.db

# 이체 테이블 확인
.tables
SELECT * FROM transfer LIMIT 10;
```

**API 디버깅**:
- FastAPI 자동 문서: http://localhost:8000/docs
- 개발자 도구 Network 탭에서 요청/응답 확인

### 프론트엔드 디버깅

**React 개발자 도구**:
- 브라우저 확장 프로그램 설치
- 컴포넌트 상태 및 props 확인

**네트워크 요청 확인**:
```javascript
// transferAPI.ts에서 디버깅
console.log('Transfer request:', requestData);
console.log('Transfer response:', response);
```

**스타일 디버깅**:
```bash
# Tailwind CSS 클래스 확인
npm run dev
# 브라우저 개발자 도구 Elements 탭에서 확인
```

## 테스트 실행

### 백엔드 테스트

```bash
cd backend

# 전체 테스트 실행
pytest

# 이체 관련 테스트만 실행
pytest tests/unit/test_transfer_service.py
pytest tests/integration/test_transfer_api.py

# 커버리지 포함 테스트
pytest --cov=src tests/
```

### 프론트엔드 테스트

```bash
cd frontend

# 전체 테스트 실행
npm test

# 이체 컴포넌트 테스트만 실행
npm test -- TransferForm

# 테스트 커버리지 확인
npm run test:coverage
```

## 문제 해결

### 자주 발생하는 오류

**1. 데이터베이스 연결 오류**
```
sqlite3.OperationalError: no such table: transfer
```
해결: 데이터베이스 마이그레이션 실행
```bash
cd backend
python -m src.database.migrations.create_transfer_tables
```

**2. 포트 충돌 오류**
```
Error: Port 8000 already in use
```
해결: 기존 프로세스 종료 또는 다른 포트 사용
```bash
# 프로세스 확인
lsof -i :8000

# 프로세스 종료
kill -9 <PID>
```

**3. 모듈 임포트 오류**
```
ModuleNotFoundError: No module named 'src'
```
해결: Python 경로 설정 확인
```bash
cd backend
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### 로그 파일 위치

- **백엔드 로그**: `backend/logs/app.log`
- **프론트엔드 로그**: 브라우저 개발자 도구 Console
- **데이터베이스 로그**: `database/logs/sqlite.log`

## 다음 단계

1. **구현 태스크 확인**: `specs/002-transfer/tasks.md` (생성 예정)
2. **상세 구현 가이드**: 각 컴포넌트별 구현 문서 참조
3. **통합 테스트**: 전체 이체 플로우 테스트
4. **성능 최적화**: API 응답 시간 측정 및 개선

## 추가 리소스

- **API 명세서**: `specs/002-transfer/contracts/api.yaml`
- **데이터 모델**: `specs/002-transfer/data-model.md`
- **아키텍처 연구**: `specs/002-transfer/research.md`
- **구현 계획**: `specs/002-transfer/plan.md`

## 지원

문제가 발생하거나 질문이 있으면 다음을 확인하세요:
1. 이 문서의 문제 해결 섹션
2. API 문서 (http://localhost:8000/docs)
3. 관련 스펙 문서들
4. 기존 거래 내역 기능 구현 참조