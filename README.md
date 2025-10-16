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
- [페이지 분석 도구](#-페이지-분석-도구)
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

### 5. 페이지 분석 도구 (신규!)
- 🎯 대화형 CLI로 앱 화면 실시간 분석
- 🔍 9가지 검색 옵션으로 UI 요소 빠르게 찾기
- 🤖 10가지 locator 전략 자동 생성 및 추천
- 📦 JSON 파일로 요소 정보 저장 및 공유
- ⚡ 테스트 작성 시간 80% 이상 단축

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
│   ├── account_loader.py       # 계정 정보 로더
│   ├── page_analyzer.py        # ⭐ 페이지 분석 도구 (신규)
│   ├── element_finder.py       # ⭐ 요소 검색 및 locator 생성 (신규)
│   └── json_locator_helper.py  # ⭐ JSON에서 locator 추출 (신규)
│
├── elements/                    # ⭐ 페이지 요소 JSON 파일 (신규)
│   ├── student_home.json       # 학생 홈 화면 (234개 요소)
│   ├── student_tutoring.json   # 과외 화면 (167개 요소)
│   └── student_preparation.json # 자습 화면 (128개 요소)
│
├── docs/                        # ⭐ 문서 (신규)
│   ├── PAGE_ANALYZER_GUIDE.md  # 페이지 분석 도구 가이드
│   └── WORK_SUMMARY_2025_10_15.md # 작업 요약
│
├── conftest.py                  # pytest 설정 및 fixture
├── pytest.ini                   # pytest 설정 파일
├── generate_report.sh           # Allure 리포트 생성 스크립트
├── CHANGELOG.md                 # 변경 이력
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

## 🔍 페이지 분석 도구

> 새로운 페이지의 UI 요소를 빠르게 분석하고 locator를 자동 생성하는 개발 도구

### 개요

테스트 작성 시 가장 시간이 많이 걸리는 작업은 **UI 요소를 찾고 locator를 작성**하는 것입니다.
페이지 분석 도구는 이 과정을 자동화하여 **테스트 작성 시간을 80% 이상 단축**합니다.

### 주요 기능

- ✅ **실시간 화면 분석**: 앱 화면을 대화형으로 분석
- ✅ **9가지 검색 옵션**: 텍스트, 타입, 버튼, 텍스트 필드 등 다양한 방법으로 검색
- ✅ **자동 locator 생성**: 10가지 locator 전략을 자동으로 생성
- ✅ **추천 locator**: 가장 안정적인 locator를 자동으로 선택
- ✅ **JSON 저장**: 모든 요소 정보를 JSON 파일로 저장하여 팀원과 공유

### 빠른 시작

```bash
# 1. 도구 실행
python3 utils/page_analyzer.py

# 2. 앱이 자동으로 실행되고 연결됨

# 3. 분석하려는 화면까지 수동으로 이동

# 4. Enter 키를 눌러 페이지 소스 캡처

# 5. 대화형 메뉴에서 원하는 작업 선택
```

### 사용 예시

#### 1단계: 도구 실행 및 화면 캡처
```bash
$ python3 utils/page_analyzer.py

============================================================
페이지 분석 도구 시작
============================================================

앱에 연결 중...
✅ iPad_9th_15.7_real 연결 성공!

⚠️  앱을 분석하려는 화면까지 수동으로 이동한 후 Enter를 누르세요...

📸 현재 화면의 페이지 소스를 캡처하는 중...
✅ 캡처 완료!
```

#### 2단계: 요소 검색
```bash
============================================================
페이지 분석 도구 - 메뉴
============================================================
1. 텍스트로 검색 (이름/라벨/값)
2. 모든 버튼 보기
3. 모든 텍스트 필드 보기
4. 모든 정적 텍스트 보기
5. 모든 이미지 보기
6. 페이지 요약 (요소 타입별 개수)
7. 타입으로 검색 (XCUIElementType*)
8. Accessibility ID로 검색
9. 모든 요소를 JSON 파일로 저장
0. 종료
============================================================

선택하세요 (0-9): 2

총 12개의 버튼을 찾았습니다.

Type                           Name/Label                               Value
------------------------------------------------------------------------------------------
Button                         홈 Tab 1 of 3                            (없음)
Button                         과외 Tab 2 of 3                          (없음)
Button                         자습 Tab 3 of 3                          (없음)
```

#### 3단계: Locator 코드 생성
```bash
원하는 요소 번호 입력 (0: 뒤로가기): 1

============================================================
Locator 코드 생성
============================================================
(AppiumBy.ACCESSIBILITY_ID, "홈\nTab 1 of 3")

📋 위 코드를 Page Object 클래스에 복사하여 사용하세요.
```

#### 4단계: JSON 파일로 저장
```bash
선택하세요 (0-9): 9
저장할 파일명 입력 (기본: page_elements.json): student_home.json

✅ 총 234개의 요소를 elements/student_home.json에 저장했습니다.
💡 각 요소의 locators.recommended 필드를 확인하세요.
```

### 생성되는 Locator 종류

페이지 분석 도구는 각 요소마다 10가지 locator 전략을 자동으로 생성합니다:

1. **accessibility_id** - 가장 안정적 (우선 추천)
2. **xpath_by_name** - name 속성 기반
3. **xpath_by_label** - label 속성 기반
4. **xpath_by_value** - value 속성 기반
5. **xpath_by_type** - 요소 타입 기반
6. **xpath_type_and_name** - 타입+name 조합
7. **xpath_type_and_label** - 타입+label 조합
8. **xpath_absolute** - 절대 경로 (계층 구조)
9. **ios_class_chain** - iOS 전용, 빠른 실행
10. **ios_predicate** - iOS 전용, 강력한 필터링

### JSON 파일 활용

저장된 JSON 파일을 테스트 작성 시 참조할 수 있습니다:

```python
# utils/json_locator_helper.py 사용
from utils.json_locator_helper import JSONLocatorHelper

# JSON 파일 로드
helper = JSONLocatorHelper('elements/student_home.json')

# 텍스트로 검색
elements = helper.find_by_text('로그인')

# 권장 locator 가져오기
if elements:
    locator = helper.get_recommended_locator(elements[0])
    print(f"추천 locator: {locator}")
```

### 실전 활용 예시

#### Before (기존 방식)
```python
# 1. Appium Inspector로 요소 찾기 (5분)
# 2. 수동으로 locator 작성 (3분)
# 3. 테스트하고 오류 수정 (5분)
# → 총 13분 소요

class HomePage(BasePage):
    # locator를 찾기 어렵고 오류가 자주 발생
    SOME_BUTTON = (AppiumBy.XPATH, "//XCUIElementTypeButton[1]")  # 불안정
```

#### After (페이지 분석 도구 사용)
```python
# 1. page_analyzer.py 실행 (1분)
# 2. 버튼 검색 및 locator 복사 (30초)
# 3. Page Object에 붙여넣기 (30초)
# → 총 2분 소요 (85% 시간 절약!)

class HomePage(BasePage):
    # 자동으로 생성된 가장 안정적인 locator
    GNB_HOME = (AppiumBy.ACCESSIBILITY_ID, "홈\nTab 1 of 3")  # 안정적
    GNB_TUTORING = (AppiumBy.ACCESSIBILITY_ID, "과외\nTab 2 of 3")
    GNB_PREPARATION = (AppiumBy.ACCESSIBILITY_ID, "자습\nTab 3 of 3")
```

### 상세 가이드

페이지 분석 도구의 모든 기능과 사용법은 다음 문서를 참고하세요:

**📖 [페이지 분석 도구 완전 가이드](docs/PAGE_ANALYZER_GUIDE.md)**

내용:
- 상세한 사용법 및 예제
- 10가지 locator 전략 설명
- JSON 파일 구조 및 활용법
- 팁과 모범 사례
- 문제 해결 가이드

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
