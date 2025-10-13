# pages/my_page.py
from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage

class MyPage(BasePage):
    # --- Locators ---
    EMAIL_TEXT_FIELD = (AppiumBy.XPATH, "//XCUIElementTypeTextField")
    LOGOUT_BUTTON = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`name == "로그아웃"`]')
    EMAIL_INPUT = (AppiumBy.ACCESSIBILITY_ID, "이메일을 입력해 주세요")
    
    # --- Actions ---
    def get_logged_in_email(self):
        email_element = self.find_element(self.EMAIL_TEXT_FIELD)
        return email_element.get_attribute('value')

    def click_logout_button(self):
        print("로그아웃 버튼을 클릭합니다.")
        self.click(self.LOGOUT_BUTTON)