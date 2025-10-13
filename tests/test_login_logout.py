# tests/test_login_logout.py
import time
from appium import webdriver
from appium.options.common import AppiumOptions

# pages 에 생성된 객체들을 import 
# 테스트 스크립트에서 사용할 객체(페이지)들을 모두 import 해야 함
from pages.login_page import LoginPage
from pages.my_page import MyPage
from pages.home_page import HomePage

# -- 드라이버 설정 (이 테스트 스크립트를 실행할 디바이스의 실제 정보를 입력해야 함) --
desired_caps = { "platformName": "iOS",
    "appium:platformVersion": "15.7",
    "appium:deviceName": "DAVE의 iPad",
    "appium:automationName": "XCUITest",
    "appium:udid": "00008030-000E65282123C02E",
    "appium:app": "/Users/davekim/Downloads/iOS_App/app.ipa",
    "autoAcceptAlerts": True, # 모든 시스템 알림 팝업을 자동으로 '허용'
     
    # 미리 빌드된 WDA를 사용하라는 옵션
    "appium:usePrebuiltWDA": True,

    # WDA 빌드 파일들을 저장할 고유한 경로 지정 (다른 프로젝트와의 충돌 방지)
    # /Users/davekim/wda_build 라는 경로로 지정, 폴더는 Appium이 알아서 생성함
    # 추후 테스트 PC 설정후 Cloud 로 작업 시 변경해야 함
    "appium:derivedDataPath": "/Users/davekim/wda_build",

    # WDA가 기기에서 실행될 때까지 기다리는 시간 늘리기 (초기 설치 시 도움)
    "appium:wdaLaunchTimeout": 30000 # 30초 (단위: 밀리초)
}

APPIUM_SERVER_URL = "http://localhost:4723/wd/hub" # 추후 테스트 PC 설정후 Cloud 로 작업 시 변경해야 함

print("아이패드를 위한 Appium 드라이버를 생성합니다...")
driver = webdriver.Remote(APPIUM_SERVER_URL, options=AppiumOptions().load_capabilities(desired_caps))
print("드라이버 생성 완료.")

# -- 테스트 시나리오 --
try:
    # 페이지 객체 생성
    login_page = LoginPage(driver)
    my_page = MyPage(driver)
    home_page = HomePage(driver)

    # 테스트에 사용할 데이터
    id_key = "ssdave04@seoltab.test"
    pw_key = "asdfasdf1"

    # 여기서 부터 테스트 시나리오에 사용할 케이스들(pages에서 정의된 기능들)을 호출
    # 이어서 진행할 테스트 기능들을 pages 에서 호출해서 실행되도록 시나리오를 구성해야 함
    # 각 호출마다 주석으로 케이스를 표시하여 시나리오 가독성을 확보해야 함
    
    login_page.login(id_key, pw_key) # 로그인
    home_page.close_intro_popup() # 홈 인트로 팝업 다이얼로그 닫음
    home_page.go_to_my_page() # 홈 상단에서 마이페이지 아이콘 클릭하여 마이페이지로 이동

    # 로그인 데이터 정상 여부 검증 (Assertion)
    # my_page.py 의 get_logged_in_email() 을 호출해서 추출한 정보를 logged_in_email에 저장
    logged_in_email = my_page.get_logged_in_email() 
    print(f"마이페이지에서 확인된 이메일: {logged_in_email}")
    assert id_key == logged_in_email
    print("로그인 정보가 정상입니다.")

    my_page.click_logout_button() # 로그아웃
    
    # 로그아웃 후 로그인 페이지(로그인 버튼)가 정상 노출되었는지 확인
    login_page.verify_login_page_is_visible()
    # VERIFY: '이메일 입력창' 요소가 보이는지 확인합니다...
    #  -> PASS: '이메일 입력창' 요소가 성공적으로 노출되었습니다.
    
    # 로그아웃 후 로그인 페이지의 이메일 입력창이 다시 보이는지 확인하여 최종 검증
    assert login_page.find_element(login_page.LOGIN_BUTTON).is_displayed()
    print("로그아웃이 성공적으로 확인되었습니다.")

except Exception as e:
    print(f"테스트 실패: {e}")

finally:
    # 테스트 및 드라이버 종료
    time.sleep(3)
    driver.quit()
    print("테스트가 종료되었습니다.")