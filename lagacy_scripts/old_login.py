import time
from appium import webdriver
from appium.options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.pointer_input import PointerInput

# 사용자님께서 제공해주신, 아이패드를 위한 완벽한 설정값입니다.
desired_caps = {
    "platformName": "iOS",
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
    
}

# Appium 서버 주소
APPIUM_SERVER_URL = "http://localhost:4723/wd/hub"

# Appium 드라이버를 생성합니다.
print("아이패드를 위한 Appium 드라이버를 생성합니다...")
driver = webdriver.Remote(APPIUM_SERVER_URL, options=AppiumOptions().load_capabilities(desired_caps))
print("드라이버 생성 완료. 앱이 성공적으로 실행되었습니다.")

id_key = "ssdave04@seoltab.test"
pw_key = "asdfasdf1"

try:
    print("로그인 페이지가 노출될 때까지 최대 20초간 대기합니다...")
    wait = WebDriverWait(driver,20)    # 20초짜리 wait 타이머 생성
    # "ACCESSIBILITY_ID가 'login_button'인 요소가 '화면에 보일 때까지(visible)' 기다려.
    #  찾으면 그 요소를 login_button 변수에 담아줘!"
    id = wait.until(EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, "이메일을 입력해 주세요")))
    print("ID 입력창을 찾았습니다! 이제 로그인을 시도합니다.")
    id.send_keys(id_key)
    pw = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "비밀번호를 입력해주세요")
    pw.send_keys(pw_key)
    login_button = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "로그인")
    login_button.click()
except Exception as e:
    # 20초동안 로그인 버튼이 노출되지 않으면 에러 메시지를 출력합니다.
    print("로그인 페이지를 찾는데 실패했습니다.")

try:
    print("로그인 페이지를 찾지 못하여 인트로 팝업 노출 여부(로그인 됨)를 확인합니다.")
    # x_coord = 700
    # y_coord = 600

    # # 1. 'touch' 타입의 포인터(가상 손가락) 생성
    # pointer = PointerInput("touch", "finger")

    # # 2. ActionChains를 통해 동작을 순서대로 정의
    # actions = ActionChains(driver)
    # actions.w3c_actions.add_pointer_input("touch", "finger")
    # actions.w3c_actions.pointer_action.move_to_location(x_coord, y_coord) # 손가락을 좌표로 이동
    # actions.w3c_actions.pointer_action.pointer_down()                     # 손가락을 누름
    # actions.w3c_actions.pointer_action.pause(0.1)                         # 아주 잠깐 멈춤 (실제 탭처럼)
    # actions.w3c_actions.pointer_action.pointer_up()                       # 손가락을 땜

    # # 3. 정의된 동작 실행
    # actions.w3c_actions.perform()
    # print(f"좌표 ({x_coord}, {y_coord})를 탭했습니다.")
    intro_popup_dialog = wait.until(EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, "introPopupDialog")))
    print("인트로 팝업이 노출되었습니다. 이미 로그인이 되어 있습니다.")
    intro_close = driver.find_element(AppiumBy.IOS_CLASS_CHAIN, "**/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeImage[2]")
    intro_close.click()
    print("인트로 팝업을 닫았습니다.")

    home_button = wait.until(EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, "홈\nTab 1 of 3")))
    mypage_button = driver.find_element(AppiumBy.IOS_CLASS_CHAIN, "**/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeImage")
    mypage_button.click()
    login_id = wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//XCUIElementTypeTextField")))
    logged_id = login_id.get_attribute('value')
    print(f"현재 로그인 된 이메일: {login_id.get_attribute('value')}")
    assert id_key == logged_id
    print("로그인 정보가 정상입니다.")
    AssertionError
    logout = driver.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`name == "로그아웃"`]')
    logout.click()
    id = wait.until(EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, "이메일을 입력해 주세요")))
    print("로그아웃 되었습니다.")
except Exception as e:
    print(f"홈 버튼을 찾을수 없습니다.로그인 여부를 확인할 수 없습니다. 스크립트를 확인해주세요.{e}")

time.sleep(3) # 10초간 대기합니다.

# 드라이버를 종료합니다.
driver.quit()
print("로그인/로그아웃 테스트가 종료되었습니다. 앱을 종료했습니다.")