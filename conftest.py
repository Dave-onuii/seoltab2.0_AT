"""
pytest 설정 및 공통 fixture 정의
"""
import pytest
import time
import allure
from appium import webdriver
from appium.options.common.base import AppiumOptions

# 페이지 객체들을 import
from pages.login_page import LoginPage
from pages.my_page import MyPage
from pages.home_page import HomePage

# 헬퍼 함수를 import
from utils.capabilities_loader import get_capabilities
from utils.account_loader import get_account_credentials


def pytest_addoption(parser):
    """
    커맨드라인 옵션 추가

    사용 예시:
        pytest --device iPad_9th_15.7_real
        pytest --device galaxy_s22_real
        pytest  (기본값: iPad_9th_15.7_real)
    """
    parser.addoption(
        "--device",
        action="store",
        default="iPad_9th_15.7_real",
        help="디바이스 이름 (devices.json에 정의된 키)"
    )


@pytest.fixture(scope="function")
def device_name(request):
    """
    커맨드라인에서 전달받은 디바이스 이름을 반환하는 fixture
    """
    return request.config.getoption("--device")


@pytest.fixture(scope="function")
def driver(device_name):
    """
    Appium 드라이버 fixture
    각 테스트 함수마다 새로운 드라이버를 생성하고 종료합니다.

    scope="function": 각 테스트마다 새로 생성 (기본값)
    scope="session": 전체 테스트 세션에서 1번만 생성
    scope="module": 모듈(파일)당 1번만 생성

    Args:
        device_name: 디바이스 이름 (커맨드라인 옵션 또는 기본값)
    """
    print(f"\n[SETUP] Appium 드라이버를 생성합니다 (디바이스: {device_name})...")

    # device.json 파일에서 Capabilities 정보를 가져옵니다.
    desired_caps = get_capabilities(device_name)

    # AppiumOptions 객체를 생성하고, 가져온 정보로 로드합니다.
    options = AppiumOptions().load_capabilities(desired_caps)

    # Appium 드라이버 생성
    driver = webdriver.Remote('http://localhost:4723/wd/hub', options=options)
    print(f"[SETUP] 드라이버 생성 완료 (디바이스: {device_name}).")

    # Allure 환경 정보 추가
    allure.dynamic.parameter("디바이스", device_name)
    allure.dynamic.parameter("플랫폼", desired_caps.get("platformName", "Unknown"))
    allure.dynamic.parameter("플랫폼 버전", desired_caps.get("appium:platformVersion", "Unknown"))

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


# pytest hook: 테스트 실패 시 스크린샷 저장 및 Allure 첨부
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    테스트 실패 시 자동으로 스크린샷을 캡처하고 Allure 리포트에 첨부합니다.
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

                # Allure 리포트에 스크린샷 첨부
                with open(screenshot_name, 'rb') as image_file:
                    allure.attach(
                        image_file.read(),
                        name=f"실패 스크린샷 - {item.name}",
                        attachment_type=allure.attachment_type.PNG
                    )
                print(f"[ALLURE] 스크린샷을 Allure 리포트에 첨부했습니다.")
            except Exception as e:
                print(f"\n[ERROR] 스크린샷 저장/첨부 실패: {e}")


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
