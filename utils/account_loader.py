import json
import os

def get_account(account_name: str) -> dict:
    """
    지정된 계정 이름에 해당하는 계정 정보를 JSON 파일에서 로드합니다.

    :param account_name: accounts.json 파일에 정의된 계정 키 (예: "test_account_1")
    :return: 해당 계정의 이메일과 비밀번호 정보를 담은 딕셔너리
    """
    # 현재 파일의 경로를 기준으로 accounts.json 파일의 절대 경로를 계산합니다.
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'accounts.json')

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            all_accounts = json.load(f)

        if account_name in all_accounts:
            return all_accounts[account_name]
        else:
            raise ValueError(f"'{account_name}'에 해당하는 계정을 config/accounts.json 파일에서 찾을 수 없습니다.")

    except FileNotFoundError:
        raise FileNotFoundError("config/accounts.json 파일을 찾을 수 없습니다. 경로를 확인해주세요.")
    except json.JSONDecodeError:
        raise Exception("config/accounts.json 파일의 형식이 올바르지 않습니다.")


def get_account_credentials(account_name: str) -> tuple:
    """
    계정 정보에서 이메일과 비밀번호만 튜플로 반환합니다.

    :param account_name: accounts.json 파일에 정의된 계정 키
    :return: (email, password) 튜플
    """
    account = get_account(account_name)
    return account['email'], account['password']
