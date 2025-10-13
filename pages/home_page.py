# pages/home_page.py

from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage
from selenium.common.exceptions import TimeoutException

class HomePage(BasePage):
    """홈 화면의 UI 요소 및 관련 동작을 정의하는 클래스"""

    # --- Locators ---
    INTRO_POPUP_DIALOG = (AppiumBy.ACCESSIBILITY_ID, "introPopupDialog")
    INTRO_POPUP_CLOSE_BUTTON = (AppiumBy.IOS_CLASS_CHAIN, "**/XCUIElementTypeWindow[1]/**/XCUIElementTypeImage[2]")
    MY_PAGE_BUTTON = (AppiumBy.IOS_CLASS_CHAIN, "**/XCUIElementTypeWindow[1]/**/XCUIElementTypeImage")

    # --- Actions ---
    def close_intro_popup(self):
        """인트로 팝업이 보이면 닫는 동작"""
        try:
            # 1. 중복되던 wait_for_element 메소드를 삭제했습니다.
            # 2. 부모 클래스의 강력해진 find_element를 사용하고, timeout만 5초로 지정합니다.
            self.find_element(self.INTRO_POPUP_DIALOG, timeout=5)
            print("홈 페이지: 인트로 팝업이 노출되었습니다. 닫기를 시도합니다.")
            self.click(self.INTRO_POPUP_CLOSE_BUTTON)
            print("홈 페이지: 인트로 팝업을 닫았습니다.")
        except TimeoutException:
            print("홈 페이지: 인트로 팝업이 나타나지 않았습니다. 다음 단계로 진행합니다.")
            pass

    def go_to_my_page(self):
        """하단 탭 바에서 '마이페이지' 버튼을 클릭하는 동작"""
        print("홈 페이지: 마이페이지 버튼을 클릭합니다.")
        # 이 메소드는 기본 대기 시간(20초)을 그대로 사용합니다.
        self.click(self.MY_PAGE_BUTTON)
        print("홈 페이지: 마이페이지로 이동했습니다.")