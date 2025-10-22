import json
import os

def get_capabilities(device_name: str) -> dict:
    """
    지정된 디바이스 이름에 해당하는 Desired Capabilities를 JSON 파일에서 로드합니다.

    :param device_name: devices.json 파일에 정의된 디바이스 키 (예: "galaxy_s22_real")
    :return: 해당 디바이스의 Desired Capabilities 딕셔너리
    """
    # 현재 파일의 경로를 기준으로 devices.json 파일의 절대 경로를 계산합니다.
    # 이렇게 하면 어떤 위치에서 스크립트를 실행해도 파일 경로가 깨지지 않습니다.
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'devices.json')
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            all_devices = json.load(f)
        
        if device_name in all_devices:
            return all_devices[device_name]
        else:
            raise ValueError(f"'{device_name}'에 해당하는 디바이스를 config/devices.json 파일에서 찾을 수 없습니다.")
            
    except FileNotFoundError:
        raise FileNotFoundError("config/devices.json 파일을 찾을 수 없습니다. 경로를 확인해주세요.")
    except json.JSONDecodeError:
        raise Exception("config/devices.json 파일의 형식이 올바르지 않습니다.")