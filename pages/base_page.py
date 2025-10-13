# pages/base_page.py

# 1. import 구문을 파일 최상단으로 옮겨 코드를 깔끔하게 정리합니다.
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        # 각 메소드에서 WebDriverWait를 직접 생성하므로, __init__에서는 삭제해도 됩니다.

    # 2. find_element 메소드를 timeout 인자를 받도록 업그레이드합니다.
    #    이제 이 메소드가 wait_for_element의 역할을 완벽히 수행합니다.
    def find_element(self, locator, timeout=20):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    # 3. click과 send_keys도 timeout을 전달받을 수 있도록 수정합니다.
    def click(self, locator, timeout=20):
        """요소를 찾아 클릭합니다."""
        print(f"BasePage: '{locator}' 요소를 클릭합니다.")
        self.find_element(locator, timeout).click()

    def send_keys(self, locator, text, timeout=20):
        """요소를 찾아 텍스트를 입력합니다."""
        print(f"BasePage: '{locator}' 요소에 '{text}'를 입력합니다.")
        self.find_element(locator, timeout).send_keys(text)

    # --- ✨ 새로운 검증 전용 메서드 추가 ---
    def verify_element_visibility(self, locator, element_name, timeout=20):
        """
        요소가 보이는지 '검증'하고 성공 시 명확한 PASS 로그를 남깁니다.
        테스트 케이스의 성공/실패를 결정하는 중요한 단계에서 사용합니다.
        element_name: 로그에 표시될 요소의 이름 (예: "로그인 버튼")
        """
        print(f"VERIFY: '{element_name}' 요소가 보이는지 확인합니다...")
        try:
            element = self.find_element(locator, timeout)
            # 검증에 성공했을 때만 명확한 PASS 로그를 출력합니다.
            print(f"  -> PASS: '{element_name}' 요소가 성공적으로 노출되었습니다.")
            return element
        except Exception as e:
            # 검증에 실패하면 FAIL 로그를 남기고, 테스트 중단을 위해 에러를 다시 발생시킵니다.
            print(f"  -> FAIL: '{element_name}' 요소를 찾지 못했습니다.")
            raise e