# tests/test_login_logout.py
import time
from appium import webdriver
from appium.options.common import AppiumOptions

# 페이지 객체들을 import 합니다.
# 테스트 스크립트에서 사용할 객체(페이지)들을 모두 import 해야 합니다.
from pages.login_page import LoginPage
from pages.my_page import MyPage
from pages.home_page import HomePage

# -- 드라이버 설정 (기존 코드와 동일) --
desired_caps = { "platformName": "iOS",
    "appium:platformVersion": "15.7",
    "appium:deviceName": "DAVE의 iPad",
    "appium:automationName": "XCUITest",
    "appium:udid": "00008030-000E65282123C02E",
    "appium:app": "/Users/davekim/Downloads/iOS_App/app.ipa",
    "autoAcceptAlerts": True, # 모든 시스템 알림 팝업을 자동으로 '허용'합니다.
     
    # 1. 미리 빌드된 WDA를 사용하라는 옵션 (가장 중요!)
    # 이 옵션 하나로 복잡한 빌드 과정을 대부분 건너뛸 수 있습니다.
    "appium:usePrebuiltWDA": True,

    # 2. WDA 빌드 파일들을 저장할 고유한 경로 지정 (다른 프로젝트와의 충돌 방지)
    # /Users/davekim/wda_build 라는 경로로 지정합니다. 폴더는 Appium이 알아서 만듭니다.
    "appium:derivedDataPath": "/Users/davekim/wda_build",

    # 3. WDA가 기기에서 실행될 때까지 기다리는 시간 늘리기 (초기 설치 시 도움)
    "appium:wdaLaunchTimeout": 30000 # 30초 (단위: 밀리초)
} # 기존 설정값 그대로 복사

APPIUM_SERVER_URL = "http://localhost:4723/wd/hub"

print("아이패드를 위한 Appium 드라이버를 생성합니다...")
driver = webdriver.Remote(APPIUM_SERVER_URL, options=AppiumOptions().load_capabilities(desired_caps))
print("드라이버 생성 완료.")

# -- 테스트 시나리오 --
try:
    # 1. 페이지 객체 생성
    login_page = LoginPage(driver)
    my_page = MyPage(driver)
    home_page = HomePage(driver)

    # 2. 테스트에 사용할 데이터
    id_key = "ssdave04@seoltab.test"
    pw_key = "asdfasdf1"

    # 3. 테스트 시나리오 실행 (로그인)
    login_page.login(id_key, pw_key)
    
    # 여기서 홈 팝업 처리 로직 추가 가능
    home_page.close_intro_popup()
    home_page.go_to_my_page()

    # 4. 검증 (Assertion)
    logged_in_email = my_page.get_logged_in_email()
    print(f"마이페이지에서 확인된 이메일: {logged_in_email}")
    assert id_key == logged_in_email
    print("로그인 정보가 정상입니다.")

    # 5. 로그아웃
    my_page.click_logout_button()
    
    # ✨ 중요한 검증: 로그아웃 후 로그인 페이지가 보이는가?
    login_page.verify_login_page_is_visible()
    # -> VERIFY: '이메일 입력창' 요소가 보이는지 확인합니다...
    # ->   -> PASS: '이메일 입력창' 요소가 성공적으로 노출되었습니다.
    
    # 로그아웃 후 로그인 페이지의 이메일 입력창이 다시 보이는지 확인하여 최종 검증
    assert login_page.find_element(login_page.LOGIN_BUTTON).is_displayed()
    print("로그아웃이 성공적으로 확인되었습니다.")

except Exception as e:
    print(f"테스트 실패: {e}")

finally:
    # 6. 테스트 종료
    time.sleep(3)
    driver.quit()
    print("테스트가 종료되었습니다.")