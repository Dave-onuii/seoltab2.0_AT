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
        pytest --auto-report  (테스트 후 자동으로 Allure 리포트 생성)
    """
    parser.addoption(
        "--device",
        action="store",
        default="stg_iPad_9th_15.7_real",
        help="디바이스 이름 (devices.json에 정의된 키)"
    )
    parser.addoption(
        "--auto-report",
        action="store_true",
        default=False,
        help="테스트 종료 후 자동으로 Allure 리포트 생성"
    )
    parser.addoption(
        "--slack",
        action="store_true",
        default=False,
        help="Slack 채널에 테스트 결과 알림 전송"
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

    # Appium 드라이버 생성 (Fallback 방식)
    try:
        # 먼저 /wd/hub 없이 시도 (Appium 2.x 기본)
        driver = webdriver.Remote('http://localhost:4723', options=options)
        print(f"[SETUP] 드라이버 생성 완료 (URL: http://localhost:4723, 디바이스: {device_name}).")
    except Exception as e:
        # 실패 시 /wd/hub 경로로 재시도
        print(f"[SETUP] 첫 번째 연결 실패, /wd/hub 경로로 재시도...")
        driver = webdriver.Remote('http://localhost:4723/wd/hub', options=options)
        print(f"[SETUP] 드라이버 생성 완료 (URL: http://localhost:4723/wd/hub, 디바이스: {device_name}).")

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
    import subprocess
    import os
    import time

    print("\n" + "="*80)
    print("설탭 2.0 테스트 자동화 종료")
    print(f"종료 상태 코드: {exitstatus}")
    print("="*80)

    # 옵션 확인
    auto_report = session.config.getoption("--auto-report", default=False)
    send_slack = session.config.getoption("--slack", default=False)

    # 테스트 결과 수집 (Slack 알림용)
    test_stats = {
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "total": 0
    }

    if hasattr(session, 'testscollected'):
        test_stats["total"] = session.testscollected

    if hasattr(session, 'testsfailed'):
        test_stats["failed"] = session.testsfailed

    if hasattr(session, 'testsskipped'):
        test_stats["skipped"] = session.testsskipped

    test_stats["passed"] = test_stats["total"] - test_stats["failed"] - test_stats["skipped"]

    if not auto_report:
        print("\n💡 Allure 리포트를 자동 생성하려면: pytest --auto-report")
        print("💡 수동 생성: ./generate_report.sh 또는 allure serve allure-results")

        # Slack 알림만 보내기 (리포트 없음)
        if send_slack:
            print("\n⚠️  --slack 옵션은 --auto-report와 함께 사용해야 합니다.")
            print("💡 사용법: pytest --auto-report --slack")

        return

    # 자동 리포트 생성
    print("\n" + "="*80)
    print("📊 Allure 리포트 자동 생성 시작...")
    print("="*80)

    start_time = time.time()
    report_generated = False

    try:
        # allure-results 디렉토리 확인
        if not os.path.exists("allure-results"):
            print("⚠️  allure-results 디렉토리가 없습니다. 리포트 생성을 건너뜁니다.")
            return

        # allure 명령어 존재 여부 확인
        result = subprocess.run(
            ["which", "allure"],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print("⚠️  allure 명령어를 찾을 수 없습니다.")
            print("💡 'brew install allure'로 설치하세요.")
            return

        # Allure 리포트 생성
        print("🔄 Allure 리포트 생성 중...")
        result = subprocess.run(
            ["allure", "generate", "allure-results", "--clean", "-o", "allure-report"],
            capture_output=True,
            text=True,
            timeout=60
        )

        elapsed_time = time.time() - start_time

        if result.returncode == 0:
            print(f"✅ Allure 리포트 생성 완료! (소요 시간: {elapsed_time:.2f}초)")
            print(f"📂 위치: allure-report/index.html")
            print(f"💡 브라우저에서 보려면: allure open allure-report")
            report_generated = True
        else:
            print(f"❌ Allure 리포트 생성 실패 (소요 시간: {elapsed_time:.2f}초)")
            if result.stderr:
                print(f"에러: {result.stderr}")

    except subprocess.TimeoutExpired:
        elapsed_time = time.time() - start_time
        print(f"⏱️  Allure 리포트 생성 시간 초과 (60초 초과, {elapsed_time:.2f}초)")
    except Exception as e:
        elapsed_time = time.time() - start_time
        print(f"❌ 예상치 못한 오류 발생 (소요 시간: {elapsed_time:.2f}초): {e}")

    print("="*80)

    # Slack 알림 전송
    if send_slack and report_generated:
        from utils.slack_notifier import send_slack_notification, get_git_info

        print("\n" + "="*80)
        print("📢 Slack 알림 전송 중...")
        print("="*80)

        # CI/CD 환경 감지
        is_ci = os.getenv("CI") or os.getenv("GITHUB_ACTIONS") or os.getenv("JENKINS_HOME")

        if is_ci:
            # CI/CD 환경: 공개 리포트 URL 생성 (GitHub Pages)
            run_id = os.getenv("GITHUB_RUN_ID", "latest")
            repo_name = os.getenv("GITHUB_REPOSITORY", "Dave-onuii/seoltab2.0_AT").split("/")[1]
            repo_owner = os.getenv("GITHUB_REPOSITORY", "Dave-onuii/seoltab2.0_AT").split("/")[0]
            report_url = f"https://{repo_owner}.github.io/{repo_name}/reports/{run_id}/index.html"
            environment = "GitHub Actions"
        else:
            # 로컬 환경: 리포트 URL은 None (메시지에서 제외됨)
            report_url = None
            environment = "로컬"

        # 테스트 결과 정보
        test_result = {
            **test_stats,
            "duration": elapsed_time,
            "exit_status": exitstatus,
            "environment": environment,
            **get_git_info()
        }

        # Slack 알림 전송
        send_slack_notification(report_url, test_result)
        print("="*80)
