"""
요소 찾기 헬퍼 - 페이지 소스에서 요소를 쉽게 검색
"""
try:
    from lxml import etree as ET
    USING_LXML = True
except ImportError:
    import xml.etree.ElementTree as ET
    USING_LXML = False

import json
from typing import List, Dict


class ElementFinder:
    """페이지 소스 XML에서 요소를 검색하는 헬퍼 클래스"""

    def __init__(self, page_source: str):
        """
        Args:
            page_source: driver.page_source로 얻은 XML 문자열
        """
        if USING_LXML:
            self.root = ET.fromstring(page_source.encode('utf-8'))
        else:
            self.root = ET.fromstring(page_source)

        # xml.etree.ElementTree용 부모 맵 생성
        if not USING_LXML:
            self.parent_map = {c: p for p in self.root.iter() for c in p}

    def find_by_text(self, text: str, case_sensitive: bool = False) -> List[Dict]:
        """
        텍스트로 요소 검색

        Args:
            text: 검색할 텍스트
            case_sensitive: 대소문자 구분 여부

        Returns:
            찾은 요소들의 정보 리스트
        """
        results = []
        search_text = text if case_sensitive else text.lower()

        for elem in self.root.iter():
            # name, label, value 속성에서 검색
            for attr in ['name', 'label', 'value']:
                elem_text = elem.get(attr, '')
                if not case_sensitive:
                    elem_text = elem_text.lower()

                if search_text in elem_text:
                    results.append(self._element_to_dict(elem))
                    break

        return results

    def find_by_type(self, element_type: str) -> List[Dict]:
        """
        요소 타입으로 검색

        Args:
            element_type: 요소 타입 (예: XCUIElementTypeButton)

        Returns:
            찾은 요소들의 정보 리스트
        """
        results = []
        for elem in self.root.iter():
            if elem.get('type') == element_type:
                results.append(self._element_to_dict(elem))
        return results

    def find_buttons(self) -> List[Dict]:
        """모든 버튼 찾기"""
        return self.find_by_type('XCUIElementTypeButton')

    def find_text_fields(self) -> List[Dict]:
        """모든 텍스트 입력 필드 찾기"""
        return self.find_by_type('XCUIElementTypeTextField')

    def find_static_texts(self) -> List[Dict]:
        """모든 정적 텍스트 찾기"""
        return self.find_by_type('XCUIElementTypeStaticText')

    def find_images(self) -> List[Dict]:
        """모든 이미지 찾기"""
        return self.find_by_type('XCUIElementTypeImage')

    def find_by_accessibility_id(self, accessibility_id: str) -> List[Dict]:
        """
        Accessibility ID로 검색

        Args:
            accessibility_id: 검색할 accessibility ID

        Returns:
            찾은 요소들의 정보 리스트
        """
        results = []
        for elem in self.root.iter():
            if elem.get('name') == accessibility_id:
                results.append(self._element_to_dict(elem))
        return results

    def get_page_summary(self) -> Dict:
        """
        페이지 요약 정보

        Returns:
            요소 타입별 개수
        """
        summary = {}
        for elem in self.root.iter():
            elem_type = elem.get('type', 'Unknown')
            summary[elem_type] = summary.get(elem_type, 0) + 1
        return summary

    def _element_to_dict(self, elem, include_locators: bool = False) -> Dict:
        """
        XML 요소를 딕셔너리로 변환

        Args:
            elem: XML 요소
            include_locators: locator 정보 포함 여부 (JSON 저장 시)

        Returns:
            요소 정보 딕셔너리
        """
        element_dict = {
            'type': elem.get('type', ''),
            'name': elem.get('name', ''),
            'label': elem.get('label', ''),
            'value': elem.get('value', ''),
            'enabled': elem.get('enabled', ''),
            'visible': elem.get('visible', ''),
            'x': elem.get('x', ''),
            'y': elem.get('y', ''),
            'width': elem.get('width', ''),
            'height': elem.get('height', ''),
        }

        # JSON 저장 시 locator 정보 추가
        if include_locators:
            element_dict['locators'] = self._generate_all_locators(elem, element_dict)

        return element_dict

    def _generate_all_locators(self, elem, element_dict: Dict) -> Dict:
        """
        요소에 사용 가능한 모든 locator 생성

        Args:
            elem: XML 요소
            element_dict: 요소 정보 딕셔너리

        Returns:
            locator 딕셔너리 (추천 locator + 모든 가능한 옵션)
        """
        locators = {
            'recommended': None,
            'accessibility_id': None,
            'xpath_by_name': None,
            'xpath_by_label': None,
            'xpath_by_type': None,
            'xpath_by_value': None,
            'xpath_absolute': None,
            'ios_class_chain': None,
            'ios_predicate': None
        }

        name = element_dict.get('name', '').strip()
        label = element_dict.get('label', '').strip()
        value = element_dict.get('value', '').strip()
        elem_type = element_dict.get('type', '')

        # 1. Accessibility ID (name 속성)
        if name:
            locators['accessibility_id'] = f'(AppiumBy.ACCESSIBILITY_ID, "{name}")'
            locators['recommended'] = locators['accessibility_id']  # 가장 안정적

        # 2. XPath - name 속성
        if name:
            locators['xpath_by_name'] = f'(AppiumBy.XPATH, "//*[@name=\\"{name}\\"]")'
            if not locators['recommended']:
                locators['recommended'] = locators['xpath_by_name']

        # 3. XPath - label 속성
        if label:
            locators['xpath_by_label'] = f'(AppiumBy.XPATH, "//*[@label=\\"{label}\\"]")'
            if not locators['recommended']:
                locators['recommended'] = locators['xpath_by_label']

        # 4. XPath - value 속성
        if value:
            escaped_value = value.replace('"', '\\"').replace('\n', '\\n')
            locators['xpath_by_value'] = f'(AppiumBy.XPATH, "//*[@value=\\"{escaped_value}\\"]")'

        # 5. XPath - type만 사용
        if elem_type:
            locators['xpath_by_type'] = f'(AppiumBy.XPATH, "//{elem_type}")'

        # 6. XPath - type + name 조합 (더 구체적)
        if elem_type and name:
            locators['xpath_type_and_name'] = f'(AppiumBy.XPATH, "//{elem_type}[@name=\\"{name}\\"]")'

        # 7. XPath - type + label 조합
        if elem_type and label:
            locators['xpath_type_and_label'] = f'(AppiumBy.XPATH, "//{elem_type}[@label=\\"{label}\\"]")'

        # 8. Absolute XPath (계층 구조)
        absolute_xpath = self._get_absolute_xpath(elem)
        if absolute_xpath:
            locators['xpath_absolute'] = f'(AppiumBy.XPATH, "{absolute_xpath}")'

        # 9. iOS Class Chain (iOS 전용, 빠름)
        if elem_type:
            short_type = elem_type.replace('XCUIElementType', '')
            if name:
                locators['ios_class_chain'] = f'(AppiumBy.IOS_CLASS_CHAIN, "**/XCUIElementType{short_type}[`name == \\"{name}\\"`]")'
            else:
                locators['ios_class_chain'] = f'(AppiumBy.IOS_CLASS_CHAIN, "**/XCUIElementType{short_type}")'

        # 10. iOS Predicate String (iOS 전용, 강력)
        predicates = []
        if name:
            predicates.append(f'name == "{name}"')
        if label:
            predicates.append(f'label == "{label}"')
        if value:
            escaped_value = value.replace('"', '\\"')
            predicates.append(f'value == "{escaped_value}"')

        if predicates:
            predicate_str = ' AND '.join(predicates)
            locators['ios_predicate'] = f'(AppiumBy.IOS_PREDICATE, "{predicate_str}")'

        # recommended가 아직 없으면 type 기반으로 설정
        if not locators['recommended'] and elem_type:
            locators['recommended'] = locators['xpath_by_type']

        return locators

    def _get_absolute_xpath(self, elem) -> str:
        """
        요소의 절대 XPath 경로 생성

        Args:
            elem: XML 요소

        Returns:
            절대 XPath 문자열
        """
        path = []
        current = elem

        # 루트까지 역순으로 탐색
        while current is not None:
            # 부모 요소 가져오기 (lxml 또는 ElementTree)
            if USING_LXML:
                parent = current.getparent()
            else:
                parent = self.parent_map.get(current)

            # 형제 요소들 가져오기
            if parent is not None:
                siblings = list(parent)
            else:
                siblings = [current]

            # 같은 타입의 형제 중에서 몇 번째인지 계산
            same_type_siblings = [s for s in siblings if s.get('type') == current.get('type')]

            if len(same_type_siblings) > 1:
                index = same_type_siblings.index(current) + 1
                path.insert(0, f"{current.get('type', '*')}[{index}]")
            else:
                path.insert(0, current.get('type', '*'))

            # 다음 부모로 이동
            current = parent
            if current is None or current == self.root:
                break

        return '/' + '/'.join(path) if path else None

    def generate_locator_code(self, element: Dict) -> str:
        """
        요소 정보로 Python 코드 생성

        Args:
            element: 요소 정보 딕셔너리

        Returns:
            Page Object용 Python 코드
        """
        name = element.get('name', '')
        label = element.get('label', '')
        elem_type = element.get('type', '')

        # 적절한 locator 전략 선택
        if name:
            return f'(AppiumBy.ACCESSIBILITY_ID, "{name}")'
        elif label:
            return f'(AppiumBy.ACCESSIBILITY_ID, "{label}")'
        elif elem_type:
            return f'(AppiumBy.IOS_CLASS_CHAIN, "**/XCUIElementType{elem_type.split("XCUIElementType")[1]}")'
        else:
            return '# 적절한 locator를 찾을 수 없습니다'

    def export_to_json(self, output_file: str, include_locators: bool = True):
        """
        모든 요소를 JSON 파일로 저장

        Args:
            output_file: 저장할 파일 경로
            include_locators: locator 정보 포함 여부 (기본값: True)
        """
        all_elements = []
        for elem in self.root.iter():
            all_elements.append(self._element_to_dict(elem, include_locators=include_locators))

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_elements, f, ensure_ascii=False, indent=2)

        print(f"[INFO] 총 {len(all_elements)}개의 요소를 {output_file}에 저장했습니다.")
        if include_locators:
            print(f"[INFO] 각 요소의 locators.recommended 필드를 확인하세요.")


def print_elements_table(elements: List[Dict], max_rows: int = 20):
    """
    요소 리스트를 테이블 형식으로 출력

    Args:
        elements: 요소 리스트
        max_rows: 최대 출력 행 수
    """
    if not elements:
        print("요소를 찾지 못했습니다.")
        return

    print(f"\n총 {len(elements)}개의 요소를 찾았습니다.\n")
    print(f"{'Type':<30} {'Name/Label':<40} {'Value':<20}")
    print("-" * 90)

    for i, elem in enumerate(elements[:max_rows]):
        elem_type = elem['type'].replace('XCUIElementType', '')
        name_label = elem['name'] or elem['label'] or '(없음)'
        value = elem['value'][:18] + '...' if len(elem['value']) > 18 else elem['value']

        print(f"{elem_type:<30} {name_label:<40} {value:<20}")

    if len(elements) > max_rows:
        print(f"\n... 및 {len(elements) - max_rows}개 더")
