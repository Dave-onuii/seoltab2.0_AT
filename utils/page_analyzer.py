#!/usr/bin/env python3
"""
페이지 분석 도구 - 새로운 페이지의 요소를 쉽게 찾고 locator 코드를 생성합니다.

사용법:
1. 앱을 원하는 화면까지 수동으로 진행
2. 이 스크립트 실행
3. 대화형 메뉴로 요소 검색 및 locator 코드 생성

예시:
    python3 utils/page_analyzer.py
"""
import sys
from pathlib import Path

# 프로젝트 루트를 Python path에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from appium import webdriver
from appium.options.common import AppiumOptions
from utils.capabilities_loader import get_capabilities
from utils.element_finder import ElementFinder, print_elements_table
import json


def print_menu():
    """메뉴 출력"""
    print("\n" + "="*60)
    print("페이지 분석 도구 - 메뉴")
    print("="*60)
    print("1. 텍스트로 검색 (이름/라벨/값)")
    print("2. 모든 버튼 보기")
    print("3. 모든 텍스트 필드 보기")
    print("4. 모든 정적 텍스트 보기")
    print("5. 모든 이미지 보기")
    print("6. 페이지 요약 (요소 타입별 개수)")
    print("7. 타입으로 검색 (XCUIElementType*)")
    print("8. Accessibility ID로 검색")
    print("9. 모든 요소를 JSON 파일로 저장")
    print("0. 종료")
    print("="*60)


def generate_locator_for_element(finder, element):
    """선택한 요소의 locator 코드 생성"""
    print("\n" + "="*60)
    print("Locator 코드 생성")
    print("="*60)
    locator_code = finder.generate_locator_code(element)

    print("\n📋 Page Object에 추가할 코드:")
    print("-" * 60)

    # 요소 이름 제안
    elem_type = element['type'].replace('XCUIElementType', '').upper()
    name_suggestion = element.get('name') or element.get('label') or 'ELEMENT'
    name_suggestion = name_suggestion.replace(' ', '_').replace('\n', '_')

    print(f"    {elem_type}_{name_suggestion} = {locator_code}")
    print("-" * 60)


def main():
    print("="*60)
    print("페이지 분석 도구 시작")
    print("="*60)

    # Appium 연결
    print("\n앱에 연결 중...")
    device_name = "iPad_9th_15.7_real"  # 필요시 변경
    desired_caps = get_capabilities(device_name)
    options = AppiumOptions().load_capabilities(desired_caps)
    driver = webdriver.Remote('http://localhost:4723/wd/hub', options=options)

    print(f"✅ {device_name} 연결 성공!")
    print("\n⚠️  앱을 분석하려는 화면까지 수동으로 이동한 후 Enter를 누르세요...")
    input()

    try:
        while True:
            # 현재 페이지 소스 가져오기
            print("\n📸 현재 화면의 페이지 소스를 캡처하는 중...")
            page_source = driver.page_source
            finder = ElementFinder(page_source)
            print("✅ 캡처 완료!\n")

            print_menu()
            choice = input("\n선택하세요 (0-9): ").strip()

            if choice == '0':
                print("\n종료합니다...")
                break

            elif choice == '1':
                search_text = input("검색할 텍스트 입력: ").strip()
                case_sensitive = input("대소문자 구분? (y/n, 기본: n): ").strip().lower() == 'y'
                results = finder.find_by_text(search_text, case_sensitive)
                print_elements_table(results)

                if results:
                    idx = input("\nlocator 코드 생성할 요소 번호 (Enter=건너뛰기): ").strip()
                    if idx.isdigit() and 0 <= int(idx) < len(results):
                        generate_locator_for_element(finder, results[int(idx)])

            elif choice == '2':
                results = finder.find_buttons()
                print_elements_table(results)

                if results:
                    idx = input("\nlocator 코드 생성할 버튼 번호 (Enter=건너뛰기): ").strip()
                    if idx.isdigit() and 0 <= int(idx) < len(results):
                        generate_locator_for_element(finder, results[int(idx)])

            elif choice == '3':
                results = finder.find_text_fields()
                print_elements_table(results)

                if results:
                    idx = input("\nlocator 코드 생성할 필드 번호 (Enter=건너뛰기): ").strip()
                    if idx.isdigit() and 0 <= int(idx) < len(results):
                        generate_locator_for_element(finder, results[int(idx)])

            elif choice == '4':
                results = finder.find_static_texts()
                print_elements_table(results)

            elif choice == '5':
                results = finder.find_images()
                print_elements_table(results)

            elif choice == '6':
                summary = finder.get_page_summary()
                print("\n페이지 요약 (요소 타입별 개수):")
                print("="*60)
                for elem_type, count in sorted(summary.items(), key=lambda x: x[1], reverse=True):
                    short_type = elem_type.replace('XCUIElementType', '')
                    print(f"  {short_type:<40} {count:>4}개")
                print("="*60)

            elif choice == '7':
                elem_type = input("검색할 타입 입력 (예: XCUIElementTypeButton): ").strip()
                results = finder.find_by_type(elem_type)
                print_elements_table(results)

                if results:
                    idx = input("\nlocator 코드 생성할 요소 번호 (Enter=건너뛰기): ").strip()
                    if idx.isdigit() and 0 <= int(idx) < len(results):
                        generate_locator_for_element(finder, results[int(idx)])

            elif choice == '8':
                accessibility_id = input("Accessibility ID 입력: ").strip()
                results = finder.find_by_accessibility_id(accessibility_id)
                print_elements_table(results)

                if results:
                    idx = input("\nlocator 코드 생성할 요소 번호 (Enter=건너뛰기): ").strip()
                    if idx.isdigit() and 0 <= int(idx) < len(results):
                        generate_locator_for_element(finder, results[int(idx)])

            elif choice == '9':
                filename = input("저장할 파일명 입력 (기본: page_elements.json): ").strip()
                if not filename:
                    filename = "page_elements.json"
                if not filename.endswith('.json'):
                    filename += '.json'

                output_path = project_root / filename
                finder.export_to_json(str(output_path))

            else:
                print("❌ 잘못된 선택입니다. 다시 선택해주세요.")

            # 다음 화면으로 이동하려면?
            continue_choice = input("\n다른 화면을 분석하시겠습니까? (y/n): ").strip().lower()
            if continue_choice != 'y':
                break

    except KeyboardInterrupt:
        print("\n\n사용자에 의해 중단되었습니다.")
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n앱 종료 중...")
        driver.quit()
        print("✅ 종료 완료")


if __name__ == "__main__":
    main()
