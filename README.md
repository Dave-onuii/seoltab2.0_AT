# seoltab2.0_AT
설탭 2.0 테스트 자동화 by.Appium(Python)

# Manual
설탭 앱 자동화 스크립트는 POM(Page Object Model) 기반으로 작성되어야 합니다.
따라서 다음의 규칙을 준수하며 작성해야 합니다.
Pages 폴더 : 테스트 할 화면 단위의 Element의 주소(locators), 테스트 할 페이지에서 동작하는 기능(def)
Tests 폴더 : 테스트 할 시나리오, Pages 폴더 별로 정의된 locators 와 기능을 조합하여 하나의 테스트 시나리오를 완성합니다.

# 주의사항
하나의 Repository 에서 여러명이 작업해야 하기 때문에 작업 전 항상 아래와 같은 절차로 진행되어야 합니다.
1. 최초 한 번만
GitHub에 생성된 Repository 주소를 복사하여 VS Code의 "Clone Repository" 기능을 통해 프로젝트를 자신의 컴퓨터로 내려받습니다.

2. 매일 반복되는 작업
작업 시작 전: 최신 코드 받기 (Pull)
코드를 수정하기 전에 항상 팀원들이 작업한 최신 내용을 먼저 받아옵니다.
VS Code 하단 상태 바의 **새로고침 모양 아이콘(Sync Changes)**을 클릭하여 Pull 받습니다.

3. 코드 수정 및 개발 (Edit)
자신의 파트를 맡아 코드를 작성하고 수정합니다.
변경 사항 저장 준비 (Stage)
Source Control 탭으로 가면 수정한 파일 목록이 "Changes"에 나타납니다.
저장하고 싶은 파일 옆의 + (Stage Changes) 버튼을 눌러 저장할 목록에 올립니다.

4. 변경 사항 확정 및 기록 (Commit)
상단의 Message 입력창에 어떤 작업을 했는지 명확하게 메시지를 작성합니다. (예: "마이페이지 로그아웃 기능 추가")
체크 ✔️ (Commit) 버튼을 누릅니다. 이 작업은 내 컴퓨터에 변경 기록을 '저장'하는 것입니다.

5. 내 작업 내용 공유하기 (Push)
내 컴퓨터에 저장(Commit)한 내용을 이제 GitHub 서버(원격 Repository)에 올려서 팀원들에게 공유합니다.
다시 하단 상태 바의 **새로고침 모양 아이콘(Sync Changes)**을 클릭하여 Push 합니다.
