# pages/home_page.py

from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage
from selenium.common.exceptions import TimeoutException

class HomePage(BasePage):
    
    # --- Locators ---
    INTRO_POPUP_DIALOG = (AppiumBy.ACCESSIBILITY_ID, "introPopupDialog")
    INTRO_POPUP_CLOSE_BUTTON = (AppiumBy.IOS_CLASS_CHAIN, "**/XCUIElementTypeWindow[1]/**/XCUIElementTypeImage[2]")
    GNB_HOME = (AppiumBy.ACCESSIBILITY_ID, '\"홈\nTab 1 of 3\"')
    GNB_TUTORING = (AppiumBy.ACCESSIBILITY_ID, '\"과외\nTab 2 of 3\"')
    GNB_PREPARATION = (AppiumBy.ACCESSIBILITY_ID, '\"자습\nTab 3 of 3\"')
    MY_PAGE_BUTTON = (AppiumBy.IOS_CLASS_CHAIN, "**/XCUIElementTypeWindow[1]/**/XCUIElementTypeImage")

    # --- Actions ---
    def close_intro_popup(self): 
        """인트로 팝업이 열리면 닫는 액션"""
        try:
            self.find_element(self.INTRO_POPUP_DIALOG, timeout=5)
            print("홈 페이지: 인트로 팝업이 노출되었습니다. 닫기를 시도합니다.")
            self.click(self.INTRO_POPUP_CLOSE_BUTTON)
            print("홈 페이지: 인트로 팝업을 닫았습니다.")
        except TimeoutException:
            print("홈 페이지: 인트로 팝업이 나타나지 않았습니다. 다음 단계로 진행합니다.")
            pass

    def go_to_my_page(self): 
        """상단 메뉴에서 마이페이지로 진입하는 액션"""
        print("홈 페이지: 마이페이지 버튼을 클릭합니다.")
        self.click(self.MY_PAGE_BUTTON) # 별도의 timeout 을 설정하지 않으면 base_page 에서 설정해둔 시간이 default
        print("홈 페이지: 마이페이지로 이동했습니다.")