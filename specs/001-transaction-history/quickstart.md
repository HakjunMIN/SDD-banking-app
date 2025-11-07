# 뱅킹 앱 개발 시작하기

이 문서는 입출금 내역 조회 기능을 가진 모바일 뱅킹 앱 프로토타입의 개발 환경 설정과 실행 방법을 안내합니다.

## 📋 프로젝트 개요

- **목적**: 입출금 내역 조회를 위한 모바일 뱅킹 앱 프로토타입
- **주요 기능**: 거래 내역 목록 조회, 필터링, 거래 상세 정보 조회
- **기술 스택**: FastAPI + React + SQLite
- **언어**: 모든 문서는 한글로 작성

## 🏗️ 프로젝트 구조

```
bankingapp/
├── backend/                 # FastAPI 백엔드
│   ├── app/
│   │   ├── main.py         # FastAPI 애플리케이션 진입점
│   │   ├── models.py       # 데이터 모델 (SQLAlchemy)
│   │   ├── schemas.py      # Pydantic 스키마
│   │   ├── crud.py         # 데이터베이스 CRUD 작업
│   │   ├── database.py     # 데이터베이스 연결 설정
│   │   └── routers/
│   │       ├── transactions.py  # 거래 관련 API 라우터
│   │       └── accounts.py      # 계좌 관련 API 라우터
│   ├── pyproject.toml      # uv 프로젝트 설정 (권장)
│   ├── requirements.txt    # Python 의존성 (대안)
│   └── sample_data.sql    # 샘플 데이터 SQL
├── frontend/               # React 프론트엔드
│   ├── src/
│   │   ├── components/     # React 컴포넌트
│   │   ├── services/       # API 호출 서비스
│   │   ├── utils/         # 유틸리티 함수
│   │   ├── App.jsx        # 메인 앱 컴포넌트
│   │   └── main.jsx       # React 진입점
│   ├── package.json       # Node.js 의존성
│   └── vite.config.js     # Vite 설정
├── database/              # 데이터베이스 파일들
│   ├── banking_app.db     # SQLite 데이터베이스
│   └── init.sql          # 초기 스키마 생성 SQL
└── docs/                  # 문서들
    ├── api-guide.md      # API 사용 가이드
    └── deployment.md     # 배포 가이드
```

## 🔧 개발 환경 설정

### 필수 요구사항

- **Python 3.9+** (백엔드용)
- **uv** (Python 패키지 관리자) - `pip install uv` 또는 [공식 설치 가이드](https://github.com/astral-sh/uv) 참조
- **Node.js 18+** (프론트엔드용)
- **Git** (버전 관리)

### 1. 저장소 클론

```bash
git clone <repository-url>
cd bankingapp
```

### 2. 백엔드 설정

```bash
# 백엔드 디렉터리로 이동
cd backend

# uv로 Python 프로젝트 초기화 (필요시)
uv init

# Python 버전 설정 (필요시)
uv python install 3.11

# 의존성 설치 (requirements.txt 기반)
uv pip sync requirements.txt

# 또는 pyproject.toml이 있는 경우:
# uv sync

# 데이터베이스 초기화 및 샘플 데이터 삽입
uv run python -c "from app.database import init_db; init_db()"
sqlite3 ../database/banking_app.db < sample_data.sql
```

### 3. 프론트엔드 설정

```bash
# 프론트엔드 디렉터리로 이동
cd ../frontend

# 의존성 설치
npm install

# 또는 yarn 사용시:
# yarn install
```

## 🚀 애플리케이션 실행

### 백엔드 실행

```bash
# backend 디렉터리에서
cd backend
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

백엔드가 실행되면:
- API 서버: http://localhost:8000
- API 문서 (Swagger): http://localhost:8000/docs
- API 문서 (ReDoc): http://localhost:8000/redoc

### 프론트엔드 실행

```bash
# frontend 디렉터리에서
cd frontend
npm run dev

# 또는 yarn 사용시:
# yarn dev
```

프론트엔드가 실행되면:
- 웹 애플리케이션: http://localhost:5173

## 🧪 기능 테스트

### 1. API 직접 테스트

**거래 내역 목록 조회:**
```bash
curl "http://localhost:8000/api/transactions?account_id=1&limit=10"
```

**특정 유형 거래 조회:**
```bash
curl "http://localhost:8000/api/transactions?type=DEPOSIT&limit=5"
```

**기간별 거래 조회:**
```bash
curl "http://localhost:8000/api/transactions?from_date=2024-01-01&to_date=2024-12-31"
```

**거래 상세 조회:**
```bash
curl "http://localhost:8000/api/transactions/1"
```

**거래 통계 조회:**
```bash
curl "http://localhost:8000/api/transactions/summary?account_id=1"
```

### 2. 웹 애플리케이션 테스트

1. 브라우저에서 http://localhost:5173 접속
2. 거래 내역 목록이 표시되는지 확인
3. 필터링 기능 테스트:
   - 거래 유형별 필터링 (입금/출금)
   - 기간별 필터링
4. 거래 상세 정보 조회 테스트
5. 페이지네이션 동작 확인

### 3. 샘플 데이터 확인

기본 계좌 정보:
- **계좌번호**: 1234-567-890123
- **계좌명**: 메인 통장
- **현재잔액**: 1,500,000원

포함된 샘플 거래:
- 급여 입금: 3,000,000원
- 온라인 쇼핑 출금: 45,000원
- ATM 출금: 200,000원
- 카페 결제: 8,500원
- 편의점 결제: 12,300원

## 🔍 문제 해결

### 일반적인 문제들

**1. 백엔드 실행 오류**
```bash
# uv가 설치되었는지 확인
uv --version

# 의존성 재설치
uv pip sync requirements.txt --force-reinstall

# 또는 pyproject.toml 사용시:
# uv sync --force-reinstall
```

**2. 데이터베이스 연결 오류**
```bash
# 데이터베이스 파일 권한 확인
ls -la database/banking_app.db

# 데이터베이스 재초기화
rm database/banking_app.db
uv run python -c "from app.database import init_db; init_db()"
```

**3. 프론트엔드 빌드 오류**
```bash
# 노드 모듈 정리 후 재설치
rm -rf node_modules package-lock.json
npm install
```

**4. CORS 오류**
- 백엔드의 `main.py`에서 CORS 설정 확인
- 프론트엔드가 http://localhost:5173에서 실행되는지 확인

### 로그 확인

**백엔드 로그:**
```bash
# 백엔드 실행시 콘솔 출력 확인
# 또는 로그 레벨 설정
uv run uvicorn app.main:app --log-level debug --reload
```

**프론트엔드 로그:**
- 브라우저 개발자 도구 (F12) Console 탭 확인
- Network 탭에서 API 호출 상태 확인

## 📊 데이터베이스 관리

### SQLite 직접 접근

```bash
# 데이터베이스 열기
sqlite3 database/banking_app.db

# 테이블 목록 확인
.tables

# 계좌 정보 조회
SELECT * FROM accounts;

# 거래 내역 조회
SELECT * FROM transactions ORDER BY transaction_date DESC LIMIT 10;

# 데이터베이스 종료
.quit
```

### 데이터 백업

```bash
# 데이터베이스 백업
cp database/banking_app.db database/backup_$(date +%Y%m%d_%H%M%S).db

# SQL 덤프 생성
sqlite3 database/banking_app.db .dump > backup.sql
```

## 📈 성능 모니터링

### API 응답 시간 측정

```bash
# API 응답 시간 측정
time curl -s "http://localhost:8000/api/transactions" > /dev/null
```

### 메모리 사용량 확인

```bash
# 백엔드 프로세스 메모리 사용량 (uv run으로 실행된 프로세스)
ps aux | grep "uv run"

# 데이터베이스 크기 확인
ls -lh database/banking_app.db
```

## 🚀 다음 단계

1. **보안 기능 추가**: JWT 인증, API 키 관리
2. **실제 데이터베이스 연동**: PostgreSQL 또는 MySQL
3. **프로덕션 배포**: Docker, AWS/Azure 배포
4. **모바일 최적화**: PWA 기능, 반응형 디자인 개선
5. **테스트 자동화**: 단위 테스트, 통합 테스트 추가

## 📞 지원

개발 중 문제가 발생하면:

1. 이 문서의 문제 해결 섹션 확인
2. API 문서 (http://localhost:8000/docs) 참고
3. 로그 파일 및 콘솔 출력 확인
4. 프로젝트 이슈 트래커에 문제 보고

---

**참고**: 이것은 프로토타입 버전으로, 프로덕션 환경에서 사용하기 전에 보안, 성능, 안정성 검토가 필요합니다.