# 빠른 시작 가이드

> 5분 안에 페이지 분석 도구 사용하기

---

## 1️⃣ 준비 (1분)

```bash
# 프로젝트 루트로 이동
cd seoltab_AT

# 가상환경 활성화
source .venv/bin/activate

# Appium 서버 실행 (별도 터미널)
# Appium Server GUI 실행 또는:
appium
```

---

## 2️⃣ 도구 실행 (30초)

```bash
python3 utils/page_analyzer.py
```

**출력:**
```
============================================================
페이지 분석 도구 시작
============================================================

앱에 연결 중...
✅ iPad_9th_15.7_real 연결 성공!

⚠️  앱을 분석하려는 화면까지 수동으로 이동한 후 Enter를 누르세요...
```

---

## 3️⃣ 화면 분석 (2분)

### Step 1: 화면 이동
- 실제 디바이스/시뮬레이터에서 분석하려는 화면으로 이동
- 터미널에서 **Enter** 키 입력

### Step 2: 요소 검색
메뉴에서 원하는 옵션 선택:

```
1. 텍스트로 검색 (이름/라벨/값)      ← 가장 많이 사용
2. 모든 버튼 보기                   ← 버튼 찾을 때
3. 모든 텍스트 필드 보기            ← 입력 필드 찾을 때
9. 모든 요소를 JSON 파일로 저장     ← 전체 페이지 저장
```

### Step 3: Locator 복사
- 원하는 요소의 번호 입력
- 생성된 locator 코드를 복사

**예시:**
```python
(AppiumBy.ACCESSIBILITY_ID, "로그인")
```

---

## 4️⃣ Page Object에 적용 (1분)

```python
# pages/login_page.py

from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage

class LoginPage(BasePage):
    # 복사한 locator를 여기에 붙여넣기
    LOGIN_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "로그인")

    def click_login(self):
        self.click(self.LOGIN_BUTTON)
```

---

## 5️⃣ (선택) JSON 파일 활용

전체 페이지를 JSON으로 저장했다면:

```python
from utils.json_locator_helper import JSONLocatorHelper

# JSON 로드
helper = JSONLocatorHelper('elements/login_page.json')

# 요소 검색
elements = helper.find_by_text('로그인')

# 권장 locator 출력
if elements:
    print(helper.get_recommended_locator(elements[0]))
```

---

## 💡 자주 사용하는 워크플로우

### 패턴 1: 새 페이지 분석
```bash
1. python3 utils/page_analyzer.py
2. 화면 이동 → Enter
3. 옵션 9: JSON 저장
4. VSCode에서 JSON 열어서 필요한 locator 복사
```

### 패턴 2: 특정 요소만 찾기
```bash
1. python3 utils/page_analyzer.py
2. 화면 이동 → Enter
3. 옵션 1: 텍스트 검색
4. Locator 복사 → Page Object에 붙여넣기
```

### 패턴 3: 모든 버튼 목록 확인
```bash
1. python3 utils/page_analyzer.py
2. 화면 이동 → Enter
3. 옵션 2: 모든 버튼 보기
4. 필요한 버튼 선택 → Locator 복사
```

---

## 🎯 팁

### Locator 선택 우선순위
1. ✅ **accessibility_id** - 가장 안정적 (권장)
2. ✅ **xpath_by_name** - name 속성 있을 때
3. ⚠️ **xpath_absolute** - 최후의 수단 (구조 변경 시 깨짐)

### JSON 파일 명명 규칙
```
elements/
├── login_page.json          # 페이지명_page.json
├── student_home.json        # 역할_화면.json
└── teacher_dashboard.json
```

---

## 🔗 더 알아보기

- **완전 가이드**: [PAGE_ANALYZER_GUIDE.md](PAGE_ANALYZER_GUIDE.md)
- **작업 요약**: [WORK_SUMMARY_2025_10_15.md](WORK_SUMMARY_2025_10_15.md)
- **프로젝트 README**: [../README.md](../README.md)

---

**작성일**: 2025-10-15
