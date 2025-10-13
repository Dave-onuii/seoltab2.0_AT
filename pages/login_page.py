# pages/login_page.py
from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage
from selenium.common.exceptions import TimeoutException # 예외 처리를 위해 import

class LoginPage(BasePage):
    # --- Locators (요소들) ---
    EMAIL_INPUT = (AppiumBy.ACCESSIBILITY_ID, "이메일을 입력해 주세요")
    PASSWORD_INPUT = (AppiumBy.ACCESSIBILITY_ID, "비밀번호를 입력해주세요")
    LOGIN_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "로그인")
    INTRO_POPUP_DIALOG = (AppiumBy.ACCESSIBILITY_ID, "introPopupDialog")

    # --- Actions (기능들) --- 
    def login(self, email, password):
        try:
            self.find_element(self.EMAIL_INPUT, timeout=20)
            print("이미엘 입력창이 노출되었습니다. 로그인을 시도합니다...")
            self.send_keys(self.EMAIL_INPUT, email)
            self.send_keys(self.PASSWORD_INPUT, password)
            self.click(self.LOGIN_BUTTON)
            print("로그인 버튼을 클릭했습니다.")
        except TimeoutException:
            # 5초 내에 팝업이 나타나지 않으면, 이미 닫혔거나 없는 것으로 간주하고 조용히 넘어갑니다.
            print("이메일 입력창이 나타나지 않았습니다. 이미 로그인 되어 있는지 확인 합니다.")
            self.find_element(self.INTRO_POPUP_DIALOG, timeout=5)
            print("인트로 팝업이 노출되었습니다. 로그인 스크립트를 종료합니다.")
            pass # 아무것도 하지 않고 넘어갑니다.

    # 로그아웃 후, 로그인 화면이 다시 나왔는지 '검증'하기 위한 메서드를 추가합니다.
    def verify_login_page_is_visible(self):
        # BasePage에 새로 만든 검증 메서드를 호출합니다.
        # 로그에 표시될 이름("이메일 입력창")을 함께 넘겨줍니다.
        self.verify_element_visibility(self.LOGIN_BUTTON, "로그인")