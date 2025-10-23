"""
더미 테스트 파일 - 자동 리포트 생성 검증용
Appium 연결 없이 빠르게 실행되는 테스트
"""
import pytest
import allure
import time


@allure.epic("검증")
@allure.feature("더미 테스트")
@allure.story("성공 케이스")
@pytest.mark.dummy
def test_dummy_success():
    """성공하는 더미 테스트"""
    with allure.step("Step 1: 준비"):
        time.sleep(0.1)
        assert True

    with allure.step("Step 2: 실행"):
        time.sleep(0.1)
        result = 1 + 1
        allure.attach(str(result), "계산 결과", allure.attachment_type.TEXT)

    with allure.step("Step 3: 검증"):
        assert result == 2


@allure.epic("검증")
@allure.feature("더미 테스트")
@allure.story("실패 케이스")
@pytest.mark.dummy
def test_dummy_fail():
    """실패하는 더미 테스트 (주석 처리)"""
    with allure.step("Step 1: 준비"):
        time.sleep(0.1)
        assert True

    with allure.step("Step 2: 의도적인 실패"):
        # assert False, "이것은 의도적인 실패입니다"
        pass  # 실제로는 실패하지 않음


@allure.epic("검증")
@allure.feature("더미 테스트")
@allure.story("스킵 케이스")
@pytest.mark.dummy
@pytest.mark.skip(reason="스킵 테스트 예제")
def test_dummy_skip():
    """스킵되는 더미 테스트"""
    assert True


@allure.epic("검증")
@allure.feature("더미 테스트")
@allure.story("파라미터 테스트")
@pytest.mark.dummy
@pytest.mark.parametrize("value", [1, 2, 3])
def test_dummy_parametrize(value):
    """파라미터를 사용하는 더미 테스트"""
    with allure.step(f"값 {value} 검증"):
        allure.attach(str(value), "입력 값", allure.attachment_type.TEXT)
        assert value > 0
