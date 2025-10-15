"""
pytest 설정 및 공통 fixture 정의
"""
import pytest
import time
from appium import webdriver
from appium.options.common.base import AppiumOptions

# 페이지 객체들을 import
from pages.login_page import LoginPage
from pages.my_page import MyPage
from pages.home_page import HomePage

# 헬퍼 함수를 import
from utils.capabilities_loader import get_capabilities
from utils.account_loader import get_account_credentials


@pytest.fixture(scope="function")
def driver():
    """
    Appium 드라이버 fixture
    각 테스트 함수마다 새로운 드라이버를 생성하고 종료합니다.

    scope="function": 각 테스트마다 새로 생성 (기본값)
    scope="session": 전체 테스트 세션에서 1번만 생성
    scope="module": 모듈(파일)당 1번만 생성
    """
    print("\n[SETUP] Appium 드라이버를 생성합니다...")

    # device.json 파일에서 Capabilities 정보를 가져옵니다.
    desired_caps = get_capabilities("iPad_9th_15.7_real")

    # AppiumOptions 객체를 생성하고, 가져온 정보로 로드합니다.
    options = AppiumOptions().load_capabilities(desired_caps)

    # Appium 드라이버 생성
    driver = webdriver.Remote('http://localhost:4723/wd/hub', options=options)
    print("[SETUP] 드라이버 생성 완료.")

    # yield로 테스트에 driver 전달
    yield driver

    # 테스트 종료 후 정리 (teardown)
    print("\n[TEARDOWN] 테스트를 종료합니다...")
    time.sleep(3)
    driver.quit()
    print("[TEARDOWN] 드라이버를 종료했습니다.")


@pytest.fixture(scope="function")
def pages(driver):
    """
    페이지 객체들을 딕셔너리로 반환하는 fixture
    모든 페이지 객체를 한번에 사용할 수 있습니다.
    """
    return {
        'login': LoginPage(driver),
        'home': HomePage(driver),
        'my': MyPage(driver)
    }


@pytest.fixture(scope="function")
def login_page(driver):
    """로그인 페이지 객체 fixture"""
    return LoginPage(driver)


@pytest.fixture(scope="function")
def home_page(driver):
    """홈 페이지 객체 fixture"""
    return HomePage(driver)


@pytest.fixture(scope="function")
def my_page(driver):
    """마이 페이지 객체 fixture"""
    return MyPage(driver)


@pytest.fixture
def test_account():
    """
    테스트 계정 정보를 반환하는 fixture
    기본적으로 test_account_1을 반환합니다.
    """
    return get_account_credentials("test_account_1")


# pytest hook: 테스트 실패 시 스크린샷 저장
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    테스트 실패 시 자동으로 스크린샷을 캡처합니다.
    """
    # 테스트 실행
    outcome = yield
    report = outcome.get_result()

    # 테스트가 실패했고, driver fixture를 사용하는 경우
    if report.when == "call" and report.failed:
        # driver fixture 가져오기
        driver = item.funcargs.get('driver', None)
        if driver:
            try:
                # 스크린샷 저장
                screenshot_name = f"screenshots/{item.name}_{int(time.time())}.png"
                driver.save_screenshot(screenshot_name)
                print(f"\n[SCREENSHOT] 스크린샷 저장: {screenshot_name}")
            except Exception as e:
                print(f"\n[ERROR] 스크린샷 저장 실패: {e}")


def pytest_configure(config):
    """pytest 시작 시 실행되는 hook"""
    import os

    # 리포트 디렉토리 생성
    os.makedirs("reports", exist_ok=True)

    # 스크린샷 디렉토리 생성
    os.makedirs("screenshots", exist_ok=True)

    print("\n" + "="*80)
    print("설탭 2.0 테스트 자동화 시작")
    print("="*80)


def pytest_sessionfinish(session, exitstatus):
    """pytest 종료 시 실행되는 hook"""
    print("\n" + "="*80)
    print("설탭 2.0 테스트 자동화 종료")
    print(f"종료 상태 코드: {exitstatus}")
    print("="*80)
