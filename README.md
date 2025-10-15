# 설탭 2.0 테스트 자동화

> iOS 앱 자동화 테스트 프레임워크 (Appium + Python + pytest)

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Appium](https://img.shields.io/badge/Appium-2.x-purple.svg)](https://appium.io/)
[![pytest](https://img.shields.io/badge/pytest-8.4.2-green.svg)](https://docs.pytest.org/)
[![Allure](https://img.shields.io/badge/Allure-2.35.1-orange.svg)](https://docs.qameta.io/allure/)

## 📋 목차

- [프로젝트 소개](#-프로젝트-소개)
- [주요 기능](#-주요-기능)
- [프로젝트 구조](#-프로젝트-구조)
- [환경 설정](#-환경-설정)
- [테스트 실행](#-테스트-실행)
- [리포트 확인](#-리포트-확인)
- [테스트 작성 가이드](#-테스트-작성-가이드)
- [팀 협업 가이드](#-팀-협업-가이드)
- [트러블슈팅](#-트러블슈팅)

---

## 🎯 프로젝트 소개

설탭 2.0 iOS 앱의 자동화 테스트 프레임워크입니다.

### 기술 스택

- **언어**: Python 3.13
- **테스트 프레임워크**: pytest 8.4.2
- **자동화 도구**: Appium (XCUITest)
- **디자인 패턴**: POM (Page Object Model)
- **리포팅**: Allure Report, pytest-html

---

## ✨ 주요 기능

### 1. POM (Page Object Model) 기반 구조
- 테스트 로직과 페이지 요소 분리
- 유지보수 용이성 향상
- 코드 재사용성 증대

### 2. pytest 기반 테스트
- 간결한 assert 문법
- 강력한 fixture 시스템
- parametrize를 통한 데이터 주도 테스트
- 마커를 통한 테스트 선택 실행

### 3. 유연한 설정 관리
- JSON 기반 디바이스 설정
- JSON 기반 계정 관리
- 커맨드라인 옵션으로 동적 디바이스 선택

### 4. 상세한 리포팅
- **Allure Report**: 아름답고 상세한 리포트
- **pytest-html**: 간단한 HTML 리포트
- 실패 시 자동 스크린샷 캡처 및 첨부

---

## 📁 프로젝트 구조

```
seoltab_AT/
├── config/                      # 설정 파일
│   ├── devices.json            # 디바이스 설정 (여러 디바이스 관리)
│   ├── accounts.json           # 테스트 계정 정보 (git 제외)
│   └── accounts.json.example   # 계정 정보 템플릿
│
├── pages/                       # Page Object Model
│   ├── base_page.py            # 공통 메서드 (find_element, click, send_keys 등)
│   ├── login_page.py           # 로그인 페이지
│   ├── home_page.py            # 홈 페이지
│   └── my_page.py              # 마이 페이지
│
├── tests/                       # 테스트 시나리오
│   └── test_login_logout.py    # 로그인/로그아웃 테스트
│
├── utils/                       # 유틸리티 함수
│   ├── capabilities_loader.py  # Appium capabilities 로더
│   └── account_loader.py       # 계정 정보 로더
│
├── conftest.py                  # pytest 설정 및 fixture
├── pytest.ini                   # pytest 설정 파일
├── generate_report.sh           # Allure 리포트 생성 스크립트
└── README.md                    # 프로젝트 문서
```

---

## 🛠️ 환경 설정

### 1. 사전 요구사항

- **Python 3.13+**
- **Appium Server** (Appium Server GUI 또는 CLI)
- **Xcode** (iOS 테스트용)
- **실제 iOS 디바이스** 또는 시뮬레이터
- **Homebrew** (macOS)

### 2. 프로젝트 클론

```bash
git clone https://github.com/Dave-onuii/seoltab2.0_AT.git
cd seoltab_AT
```

### 3. 가상환경 생성 및 활성화

```bash
# 가상환경 생성
python3 -m venv .venv

# 가상환경 활성화
source .venv/bin/activate  # macOS/Linux
```

### 4. 의존성 설치

```bash
pip install -r requirements.txt

# 또는 수동 설치
pip install appium-python-client selenium pytest pytest-html pytest-xdist pytest-timeout allure-pytest
```

### 5. Allure 설치 (리포트용)

```bash
brew install allure
```

### 6. 계정 정보 설정

```bash
# 템플릿 복사
cp config/accounts.json.example config/accounts.json

# 실제 계정 정보로 수정
vi config/accounts.json
```

### 7. 디바이스 설정

`config/devices.json`에서 디바이스 정보 확인 및 수정:

```json
{
  "iPad_9th_15.7_real": {
    "platformName": "iOS",
    "appium:platformVersion": "15.7",
    "appium:deviceName": "DAVE의 iPad",
    "appium:automationName": "XCUITest",
    "appium:udid": "your-device-udid",
    "appium:bundleId": "com.onuii.IOS.SolTab.stg",
    "autoAcceptAlerts": true,
    "appium:usePrebuiltWDA": true,
    "appium:derivedDataPath": "/Users/davekim/wda_build",
    "appium:wdaLaunchTimeout": 30000
  }
}
```

---

## 🚀 테스트 실행

### 기본 실행

```bash
# 전체 테스트 실행
pytest

# 특정 테스트 파일 실행
pytest tests/test_login_logout.py

# 특정 테스트 함수 실행
pytest tests/test_login_logout.py::test_login_logout

# Verbose 모드
pytest -v
```

### 마커로 선택 실행

```bash
# 스모크 테스트만 실행
pytest -m smoke

# 로그인 테스트만 실행
pytest -m login

# 특정 마커 제외
pytest -m "not slow"
```

### 디바이스 지정

```bash
# 기본 디바이스로 실행 (iPad_9th_15.7_real)
pytest

# 특정 디바이스 지정
pytest --device iPad_9th_15.7_real
pytest --device iPhone_14_real
pytest --device galaxy_s22_real
```

### 병렬 실행 (빠른 실행)

```bash
# 3개의 프로세스로 병렬 실행
pytest -n 3

# 자동으로 CPU 코어 수만큼 병렬 실행
pytest -n auto
```

---

## 📊 리포트 확인

### 1. Allure 리포트 (권장)

```bash
# 테스트 실행 (allure-results 자동 생성됨)
pytest

# 리포트 생성 및 브라우저에서 열기
./generate_report.sh

# 또는 수동으로
allure generate allure-results --clean -o allure-report
allure open allure-report

# 또는 즉시 서버 실행
allure serve allure-results
```

**Allure 리포트에서 볼 수 있는 정보:**
- 📈 전체 테스트 통계 및 차트
- 📝 테스트별 상세 실행 로그
- 📸 실패 시 스크린샷 자동 첨부
- 🏷️ Epic/Feature/Story 계층 구조
- ⏱️ 실행 시간 타임라인
- 📎 첨부 파일 (테스트 데이터, 로그 등)

### 2. HTML 리포트

```bash
# pytest 실행 시 자동 생성됨
pytest

# 리포트 확인
open reports/report.html
```

---

## 📝 테스트 작성 가이드

### 1. 새로운 Page Object 추가

`pages/` 폴더에 새 파일 생성:

```python
# pages/settings_page.py
from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage

class SettingsPage(BasePage):
    # --- Locators ---
    PROFILE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "프로필")
    LOGOUT_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "로그아웃")

    # --- Actions ---
    def go_to_profile(self):
        """프로필 페이지로 이동"""
        self.click(self.PROFILE_BUTTON)

    def logout(self):
        """로그아웃 수행"""
        self.click(self.LOGOUT_BUTTON)
```

### 2. 새로운 테스트 작성

`tests/` 폴더에 새 파일 생성:

```python
# tests/test_settings.py
import pytest
import allure

@allure.epic("설정")
@allure.feature("프로필 관리")
@allure.story("프로필 조회")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.smoke
def test_view_profile(pages, test_account):
    """프로필 조회 테스트"""

    with allure.step("로그인"):
        email, password = test_account
        pages['login'].login(email, password)

    with allure.step("설정 페이지 이동"):
        pages['settings'].go_to_profile()

    with allure.step("프로필 정보 확인"):
        profile = pages['settings'].get_profile_info()
        assert profile is not None
```

### 3. Fixture 활용

```python
# conftest.py에 새 fixture 추가
@pytest.fixture
def settings_page(driver):
    """설정 페이지 fixture"""
    return SettingsPage(driver)

# 테스트에서 사용
def test_example(settings_page):
    settings_page.go_to_profile()
```

---

## 👥 팀 협업 가이드

### Git 워크플로우

#### 1. 최초 설정 (한 번만)

```bash
# 저장소 클론
git clone https://github.com/Dave-onuii/seoltab2.0_AT.git
cd seoltab_AT

# 가상환경 설정
source .venv/bin/activate
pip install -r requirements.txt

# 계정 정보 설정
cp config/accounts.json.example config/accounts.json
# accounts.json 수정
```

#### 2. 일일 작업 흐름

```bash
# 1. 작업 시작 전: 최신 코드 받기
git pull origin main

# 2. 코드 수정 및 개발
# ... 코드 작성 ...

# 3. 테스트 실행 (필수!)
pytest

# 4. 변경사항 확인
git status
git diff

# 5. 변경사항 스테이징
git add .

# 6. 커밋 (명확한 메시지 작성)
git commit -m "로그인 테스트에 에러 케이스 추가"

# 7. 푸시
git push origin main
```

### 코드 리뷰 체크리스트

- [ ] 테스트가 모두 통과하는가?
- [ ] POM 구조를 따르는가?
- [ ] Allure 데코레이터가 적절히 추가되었는가?
- [ ] 주석과 docstring이 명확한가?
- [ ] 하드코딩된 값이 없는가?
- [ ] 계정 정보가 코드에 포함되지 않았는가?

---

## 🔧 트러블슈팅

### 문제 1: `pytest: command not found`

**원인**: 가상환경이 활성화되지 않음

**해결**:
```bash
# 올바른 가상환경 활성화
source .venv/bin/activate

# 프롬프트가 (.venv)로 시작하는지 확인
```

### 문제 2: Appium 연결 실패

**원인**: Appium 서버가 실행되지 않음

**해결**:
```bash
# Appium Server GUI 실행 또는
# CLI로 실행
appium
```

### 문제 3: 디바이스를 찾을 수 없음

**원인**: UDID가 잘못되었거나 디바이스 연결 안됨

**해결**:
```bash
# 연결된 디바이스 확인
xcrun xctrace list devices

# devices.json의 udid 업데이트
```

### 문제 4: WDA 빌드 실패

**원인**: WDA 설정 문제

**해결**:
```bash
# derivedDataPath 확인 및 삭제
rm -rf /Users/davekim/wda_build

# Appium 재시작
```

### 문제 5: 요소를 찾을 수 없음

**원인**: Locator가 변경되었거나 대기 시간 부족

**해결**:
```python
# timeout 증가
self.find_element(locator, timeout=30)

# 디버깅용 페이지 소스 확인
python3 tests/debug_page_source.py
```

---

## 📚 추가 문서

- [테스트 작성 상세 가이드](docs/TEST_GUIDE.md)
- [트러블슈팅 가이드](docs/TROUBLESHOOTING.md)
- [CHANGELOG](CHANGELOG.md)

---

## 🤝 기여하기

1. 이슈 등록 또는 기능 제안
2. 브랜치 생성 (선택사항)
3. 코드 작성 및 테스트
4. Pull Request 생성
5. 코드 리뷰 후 병합

---

## 📄 라이센스

이 프로젝트는 내부 프로젝트입니다.

---

## 📞 문의

- **프로젝트 관리자**: Dave Kim
- **이슈 등록**: [GitHub Issues](https://github.com/Dave-onuii/seoltab2.0_AT/issues)

---

## 🎓 참고 자료

- [Appium 공식 문서](https://appium.io/docs/)
- [pytest 공식 문서](https://docs.pytest.org/)
- [Allure 공식 문서](https://docs.qameta.io/allure/)
- [POM 패턴 가이드](https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/)
