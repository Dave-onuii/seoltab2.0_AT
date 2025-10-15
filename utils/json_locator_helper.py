#!/usr/bin/env python3
"""
JSON 파일에서 locator를 쉽게 찾는 헬퍼 유틸리티

사용 예시:
    python3 utils/json_locator_helper.py student_home.json "수강신청"
"""
import json
import sys
from typing import List, Dict


def search_elements(json_file: str, search_term: str, search_in: List[str] = None) -> List[Dict]:
    """
    JSON 파일에서 요소 검색

    Args:
        json_file: JSON 파일 경로
        search_term: 검색할 텍스트
        search_in: 검색할 필드 리스트 (기본값: ['name', 'label', 'value'])

    Returns:
        찾은 요소 리스트
    """
    if search_in is None:
        search_in = ['name', 'label', 'value']

    with open(json_file, 'r', encoding='utf-8') as f:
        elements = json.load(f)

    results = []
    search_lower = search_term.lower()

    for elem in elements:
        for field in search_in:
            field_value = elem.get(field, '').lower()
            if search_lower in field_value:
                results.append(elem)
                break

    return results


def print_locator_info(element: Dict, index: int = None):
    """
    요소의 locator 정보를 보기 좋게 출력

    Args:
        element: 요소 딕셔너리
        index: 인덱스 번호 (여러 개일 때)
    """
    if index is not None:
        print(f"\n{'='*80}")
        print(f"결과 #{index}")
        print('='*80)
    else:
        print(f"\n{'='*80}")
        print("요소 정보")
        print('='*80)

    # 기본 정보
    print(f"Type:    {element.get('type', 'N/A')}")
    print(f"Name:    {element.get('name', '(없음)')}")
    print(f"Label:   {element.get('label', '(없음)')}")
    print(f"Value:   {element.get('value', '(없음)')}")
    print(f"Enabled: {element.get('enabled', 'N/A')}")
    print(f"Visible: {element.get('visible', 'N/A')}")

    # Locator 정보
    locators = element.get('locators', {})
    if locators:
        print(f"\n📍 추천 Locator:")
        print(f"   {locators.get('recommended', 'N/A')}")

        print(f"\n🔧 사용 가능한 Locator 옵션:")
        print(f"-" * 80)

        for key, value in locators.items():
            if key != 'recommended' and value:
                print(f"  {key:<25} {value}")


def search_by_type(json_file: str, element_type: str) -> List[Dict]:
    """
    요소 타입으로 검색

    Args:
        json_file: JSON 파일 경로
        element_type: 요소 타입 (예: XCUIElementTypeButton)

    Returns:
        찾은 요소 리스트
    """
    with open(json_file, 'r', encoding='utf-8') as f:
        elements = json.load(f)

    return [elem for elem in elements if elem.get('type') == element_type]


def filter_by_visibility(elements: List[Dict], visible: bool = True) -> List[Dict]:
    """
    가시성 필터링

    Args:
        elements: 요소 리스트
        visible: True면 visible만, False면 invisible만

    Returns:
        필터링된 요소 리스트
    """
    visible_str = 'true' if visible else 'false'
    return [elem for elem in elements if elem.get('visible', '').lower() == visible_str]


def get_elements_summary(json_file: str):
    """
    JSON 파일의 요소 요약 정보 출력

    Args:
        json_file: JSON 파일 경로
    """
    with open(json_file, 'r', encoding='utf-8') as f:
        elements = json.load(f)

    print(f"\n{'='*80}")
    print(f"파일: {json_file}")
    print(f"총 요소 개수: {len(elements)}")
    print('='*80)

    # 타입별 개수
    type_counts = {}
    for elem in elements:
        elem_type = elem.get('type', 'Unknown')
        type_counts[elem_type] = type_counts.get(elem_type, 0) + 1

    print("\n요소 타입별 개수:")
    print("-" * 80)
    for elem_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
        short_type = elem_type.replace('XCUIElementType', '')
        print(f"  {short_type:<40} {count:>4}개")

    # Accessibility ID가 있는 요소
    with_name = sum(1 for elem in elements if elem.get('name', '').strip())
    print(f"\n📍 Accessibility ID(name)가 있는 요소: {with_name}개 ({with_name/len(elements)*100:.1f}%)")

    # 보이는 요소
    visible_count = len(filter_by_visibility(elements, visible=True))
    print(f"👁️  Visible=true인 요소: {visible_count}개 ({visible_count/len(elements)*100:.1f}%)")


def main():
    """메인 함수 - CLI 인터페이스"""
    if len(sys.argv) < 2:
        print("사용법:")
        print(f"  {sys.argv[0]} <json_file> [search_term]")
        print(f"\n예시:")
        print(f"  {sys.argv[0]} student_home.json              # 요약 정보")
        print(f"  {sys.argv[0]} student_home.json 수강신청      # '수강신청' 검색")
        print(f"  {sys.argv[0]} student_home.json Button       # Button 타입 검색")
        sys.exit(1)

    json_file = sys.argv[1]

    # 검색어가 없으면 요약 정보만 출력
    if len(sys.argv) < 3:
        get_elements_summary(json_file)
        return

    search_term = sys.argv[2]

    # 타입으로 검색 (XCUIElementType 로 시작하면)
    if search_term.startswith('XCUIElementType'):
        results = search_by_type(json_file, search_term)
        print(f"\n'{search_term}' 타입 검색 결과: {len(results)}개 발견")
    # 짧은 타입명으로 검색 (Button, TextField 등)
    elif search_term[0].isupper() and not ' ' in search_term:
        full_type = f"XCUIElementType{search_term}"
        results = search_by_type(json_file, full_type)
        print(f"\n'{full_type}' 타입 검색 결과: {len(results)}개 발견")
    else:
        # 텍스트 검색
        results = search_elements(json_file, search_term)
        print(f"\n'{search_term}' 검색 결과: {len(results)}개 발견")

    # 결과 출력
    if results:
        for i, elem in enumerate(results[:10], 1):  # 최대 10개만 출력
            print_locator_info(elem, index=i)

        if len(results) > 10:
            print(f"\n... 및 {len(results) - 10}개 더")
            print(f"💡 Tip: VS Code에서 {json_file}를 열어 Ctrl+F로 검색하면 모든 결과를 볼 수 있습니다.")
    else:
        print("❌ 검색 결과가 없습니다.")


if __name__ == "__main__":
    main()
