"""
로그인/로그아웃 테스트 시나리오 (pytest 버전)

이 테스트는 사용자가 성공적으로 로그인하고 로그아웃하는 전체 플로우를 검증합니다.
"""
import pytest
from utils.account_loader import get_account_credentials


@pytest.mark.smoke
@pytest.mark.login
@pytest.mark.logout
def test_login_logout(pages, test_account):
    """
    사용자가 성공적으로 로그인하고 로그아웃하는 전체 시나리오를 테스트합니다.

    Args:
        pages: 페이지 객체들 (fixture)
        test_account: 테스트 계정 정보 (fixture)
    """
    # 테스트 계정 정보
    id_key, pw_key = test_account

    # 1. 로그인 수행
    print("로그인을 시도합니다...")
    pages['login'].login(id_key, pw_key)

    # 2. 홈 화면 팝업 처리 및 마이페이지 이동
    print("홈 화면 팝업을 닫고 마이페이지로 이동합니다...")
    pages['home'].close_intro_popup()
    pages['home'].go_to_my_page()

    # 3. 로그인 데이터 정상 여부 검증 (Assertion)
    print("로그인된 이메일 정보를 검증합니다...")
    logged_in_email = pages['my'].get_logged_in_email()
    print(f"마이페이지에서 확인된 이메일: {logged_in_email}")

    # pytest의 간결한 assert 사용
    assert id_key == logged_in_email, f"로그인된 이메일이 일치하지 않습니다. 예상: {id_key}, 실제: {logged_in_email}"
    print("로그인 정보가 정상입니다.")

    # 4. 로그아웃 수행
    print("로그아웃을 시도합니다...")
    pages['my'].click_logout_button()

    # 5. 로그아웃 후 로그인 페이지가 보이는지 검증
    pages['login'].verify_login_page_is_visible()
    assert pages['login'].find_element(pages['login'].LOGIN_BUTTON).is_displayed()
    print("로그아웃이 성공적으로 확인되었습니다.")


@pytest.mark.smoke
@pytest.mark.login
def test_login_only(login_page, home_page, my_page, test_account):
    """
    로그인만 테스트하는 간단한 시나리오

    Args:
        login_page: 로그인 페이지 객체 (fixture)
        home_page: 홈 페이지 객체 (fixture)
        my_page: 마이 페이지 객체 (fixture)
        test_account: 테스트 계정 정보 (fixture)
    """
    id_key, pw_key = test_account

    # 로그인
    print("로그인을 시도합니다...")
    login_page.login(id_key, pw_key)

    # 인트로 팝업 닫기
    home_page.close_intro_popup()

    # 마이페이지 이동
    home_page.go_to_my_page()

    # 로그인 확인
    logged_in_email = my_page.get_logged_in_email()
    assert id_key == logged_in_email, "로그인된 이메일이 일치하지 않습니다."
    print(f"로그인 성공: {logged_in_email}")


# 여러 계정으로 로그인 테스트 (parametrize 사용)
@pytest.mark.parametrize("account_name", [
    "test_account_1",
    # "test_account_2",  # 추가 계정이 있으면 주석 해제
    # "admin_account",
])
@pytest.mark.login
def test_login_multiple_accounts(pages, account_name):
    """
    여러 계정으로 로그인을 테스트합니다.

    Args:
        pages: 페이지 객체들 (fixture)
        account_name: 테스트할 계정 이름
    """
    # 계정 정보 가져오기
    id_key, pw_key = get_account_credentials(account_name)

    print(f"\n[{account_name}] 계정으로 로그인을 시도합니다...")

    # 로그인
    pages['login'].login(id_key, pw_key)

    # 인트로 팝업 닫기
    pages['home'].close_intro_popup()

    # 마이페이지 이동
    pages['home'].go_to_my_page()

    # 로그인 확인
    logged_in_email = pages['my'].get_logged_in_email()
    assert id_key == logged_in_email, f"[{account_name}] 로그인된 이메일이 일치하지 않습니다."
    print(f"[{account_name}] 로그인 성공: {logged_in_email}")
