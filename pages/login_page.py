# pages/login_page.py
from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage
from selenium.common.exceptions import TimeoutException # 예외 처리를 위해 import

class LoginPage(BasePage):
    # --- Locators (요소들) ---
    EMAIL_INPUT = (AppiumBy.ACCESSIBILITY_ID, "이메일을 입력해 주세요") # 이메일 입력필드
    PASSWORD_INPUT = (AppiumBy.ACCESSIBILITY_ID, "비밀번호를 입력해주세요") # 비밀번호 입력필드
    LOGIN_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "로그인") # 로그인 버튼
    INTRO_POPUP_DIALOG = (AppiumBy.ACCESSIBILITY_ID, "introPopupDialog") # 로그인 후 홈에 진입시 노출되는 인트로 팝업 다이얼로그

    # --- Actions (기능들) --- 
    def login(self, email, password):
        """로그인 페이지가 노출되면 로그인을 진행하고 그렇지 않으면 인트로 팝업 노출여부로 로그인 여부를 체크 함"""
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

    def verify_login_page_is_visible(self): # BasePage에 만든 검증 메서드를 호출합니다.
        """로그아웃 후 로그인 페이지로 정상 랜딩되었는지 로그인 버튼 노출 여부로 확인 함"""
        self.verify_element_visibility(self.LOGIN_BUTTON, "로그인")