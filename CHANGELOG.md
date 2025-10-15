# Changelog

프로젝트의 주요 변경사항을 기록합니다.

형식은 [Keep a Changelog](https://keepachangelog.com/ko/1.0.0/)를 따르며,
버전 관리는 [Semantic Versioning](https://semver.org/lang/ko/)을 따릅니다.

---

## [Unreleased]

### 계획된 기능
- 회원가입 테스트 추가
- 비밀번호 찾기 테스트 추가
- 설정 페이지 테스트 추가
- CI/CD 파이프라인 구축
- 에러 케이스 테스트 추가

---

## [0.4.0] - 2025-10-15

### 추가됨 (Added)
- **Allure Report 시스템 통합**
  - Allure CLI 도구 설치 및 설정
  - `@allure.epic`, `@allure.feature`, `@allure.story` 데코레이터 추가
  - `allure.step()`으로 테스트 단계 구조화
  - `allure.attach()`로 테스트 데이터 자동 첨부
  - 실패 시 스크린샷 자동 첨부 기능
  - 환경 정보 자동 추가 (디바이스, 플랫폼, 버전)
- **리포트 생성 스크립트**
  - `generate_report.sh` 추가 (원클릭 리포트 생성)
- **포괄적인 문서화**
  - README.md 대폭 개선 (설치, 사용법, 트러블슈팅)
  - CHANGELOG.md 추가
  - 프로젝트 구조 문서화

### 개선됨 (Changed)
- conftest.py에 Allure 관련 기능 추가
- test_login_logout.py에 Allure 데코레이터 및 step 추가
- pytest.ini에 Allure 설정 추가

---

## [0.3.0] - 2025-10-15

### 추가됨 (Added)
- **디바이스 동적 선택 기능**
  - `--device` 커맨드라인 옵션 추가
  - pytest_addoption을 통한 디바이스 설정
  - device_name fixture 추가
  - 코드 수정 없이 여러 디바이스 테스트 가능

### 개선됨 (Changed)
- conftest.py의 driver fixture를 device_name을 받도록 수정
- 하드코딩된 디바이스명 제거

---

## [0.2.0] - 2025-10-15

### 추가됨 (Added)
- **pytest 프레임워크 전환**
  - pytest 및 관련 플러그인 설치 (pytest-html, pytest-xdist, pytest-timeout, allure-pytest)
  - pytest.ini 설정 파일 추가
  - conftest.py 추가 (fixture 시스템)
  - 마커 시스템 추가 (smoke, regression, login, logout, slow)
  - 실패 시 자동 스크린샷 캡처
  - HTML 리포트 자동 생성
- **테스트 코드 개선**
  - test_login_logout.py를 pytest 스타일로 전환
  - 3개의 테스트 함수로 분리 (login_logout, login_only, multiple_accounts)
  - parametrize를 통한 다중 계정 테스트 지원
  - test_login_logout_unittest.py로 기존 unittest 버전 백업

### 개선됨 (Changed)
- unittest 기반에서 pytest 기반으로 전환
- 간결한 assert 문법 사용
- fixture 기반 설정/해제

### 삭제됨 (Removed)
- 없음 (unittest 버전은 백업으로 보관)

---

## [0.1.0] - 2025-10-15

### 추가됨 (Added)
- **테스트 계정 관리 시스템**
  - `config/accounts.json` 추가 (여러 테스트 계정 관리)
  - `config/accounts.json.example` 템플릿 추가
  - `utils/account_loader.py` 추가
  - get_account_credentials() 함수 추가
  - .gitignore에 accounts.json 추가 (보안)

### 개선됨 (Changed)
- test_login_logout.py에서 하드코딩된 계정 정보 제거
- account_loader를 통한 동적 계정 로딩

---

## [0.0.3] - 2025-10-15

### 추가됨 (Added)
- **디바이스 설정 개선**
  - IPA 파일 경로 대신 bundleId 사용
  - 앱 실행 안정성 향상
- **로그인 요소 수정**
  - 이메일 입력필드 locator를 XPATH로 변경
  - 기존 입력값 삭제 기능 추가 (clear_first 옵션)
  - base_page.py에 clear() 메서드 추가

### 개선됨 (Changed)
- config/devices.json: app 경로 → bundleId로 변경
- pages/login_page.py: 이메일 입력필드 locator 수정
- pages/base_page.py: send_keys에 clear_first 파라미터 추가

### 수정됨 (Fixed)
- 로그인 테스트가 실패하던 문제 해결
- 이메일 필드를 찾지 못하던 문제 해결

---

## [0.0.2] - 2025-10-14

### 추가됨 (Added)
- **디버깅 파일 gitignore 추가**
  - page_source_debug.xml 제외
  - tests/debug_page_source.py 제외

---

## [0.0.1] - 2025-10-13

### 추가됨 (Added)
- **POM 기반 프로젝트 구조 수립**
  - pages/ 폴더: base_page.py, login_page.py, home_page.py, my_page.py
  - tests/ 폴더: test_login_logout.py (unittest 기반)
  - utils/ 폴더: capabilities_loader.py
  - config/ 폴더: devices.json
- **기본 테스트 시나리오**
  - 로그인/로그아웃 전체 플로우 테스트
- **기본 설정**
  - .gitignore 설정
  - README.md 초기 버전

### 기술 스택
- Python 3.13
- Appium
- unittest
- iOS (XCUITest)

---

## 버전 관리 규칙

- **MAJOR**: 호환되지 않는 API 변경
- **MINOR**: 하위 호환되는 기능 추가
- **PATCH**: 하위 호환되는 버그 수정

## 태그 형식

- `[Added]`: 새로운 기능
- `[Changed]`: 기존 기능의 변경사항
- `[Deprecated]`: 곧 제거될 기능
- `[Removed]`: 제거된 기능
- `[Fixed]`: 버그 수정
- `[Security]`: 보안 관련 수정
