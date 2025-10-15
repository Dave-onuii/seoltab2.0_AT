import unittest
import time
from appium import webdriver
from appium.options.common.base import AppiumOptions

# 페이지 객체들을 import 합니다.
from pages.login_page import LoginPage
from pages.my_page import MyPage
from pages.home_page import HomePage

# 헬퍼 함수를 import 합니다.
from utils.capabilities_loader import get_capabilities
from utils.account_loader import get_account_credentials

# unittest.TestCase를 상속받는 클래스로 전체 테스트를 묶어줍니다.
class LoginLogoutTest(unittest.TestCase):

    # setUp: 모든 테스트 메서드 실행 '전'에 딱 한 번 호출됩니다.
    def setUp(self):
        """Appium 드라이버를 생성하고 초기 페이지 객체를 설정합니다."""
        print("Appium 드라이버를 생성합니다...")
        
        # device.json 파일에서 Capabilities 정보를 가져옵니다.
        desired_caps = get_capabilities("iPad_9th_15.7_real") 
        
        # AppiumOptions 객체를 생성하고, 가져온 정보로 로드합니다.
        options = AppiumOptions().load_capabilities(desired_caps)
        
        # self.driver를 사용하여 드라이버 객체를 클래스 인스턴스 변수로 만듭니다.
        # 이렇게 해야 다른 메서드(test_..., tearDown)에서도 self.driver로 접근할 수 있습니다.
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', options=options)
        print("드라이버 생성 완료.")
        
        # 페이지 객체들도 여기서 생성해두면 편리합니다.
        self.login_page = LoginPage(self.driver)
        self.my_page = MyPage(self.driver)
        self.home_page = HomePage(self.driver)
    
    # 실제 테스트 케이스. 메서드 이름은 반드시 'test_'로 시작해야 합니다.
    def test_login_logout(self):
        """사용자가 성공적으로 로그인하고 로그아웃하는 전체 시나리오를 테스트합니다."""

        # 테스트에 사용할 계정 정보 (config/accounts.json에서 로드)
        id_key, pw_key = get_account_credentials("test_account_1")

        # 1. 로그인 수행
        print("로그인을 시도합니다...")
        self.login_page.login(id_key, pw_key)

        # 2. 홈 화면 팝업 처리 및 마이페이지 이동
        print("홈 화면 팝업을 닫고 마이페이지로 이동합니다...")
        self.home_page.close_intro_popup()
        self.home_page.go_to_my_page()

        # 3. 로그인 데이터 정상 여부 검증 (Assertion)
        print("로그인된 이메일 정보를 검증합니다...")
        logged_in_email = self.my_page.get_logged_in_email() 
        print(f"마이페이지에서 확인된 이메일: {logged_in_email}")
        self.assertEqual(id_key, logged_in_email, "로그인된 이메일이 일치하지 않습니다.")
        print("로그인 정보가 정상입니다.")

        # 4. 로그아웃 수행
        print("로그아웃을 시도합니다...")
        self.my_page.click_logout_button()
        
        # 5. 로그아웃 후 로그인 페이지가 보이는지 검증
        # ✨ 중요한 검증: 로그아웃 후 로그인 페이지가 보이는가?
        self.login_page.verify_login_page_is_visible()
        # -> VERIFY: '로그인 버튼' 요소가 보이는지 확인합니다...
        # ->   -> PASS: '로그인 버튼' 요소가 성공적으로 노출되었습니다.
        assert self.login_page.find_element(self.login_page.LOGIN_BUTTON).is_displayed()
        print("로그아웃이 성공적으로 확인되었습니다.")
               
    # tearDown: 모든 테스트 메서드 실행 '후'에 딱 한 번 호출됩니다. (테스트 실패 여부와 상관없이)
    def tearDown(self):
        """테스트가 끝난 후 드라이버를 종료합니다."""
        if self.driver:
            time.sleep(3)
            self.driver.quit()
            print("테스트가 종료되었습니다.")


# 이 파일을 직접 실행할 경우 unittest를 실행하라는 의미입니다.
if __name__ == '__main__':
    unittest.main()
