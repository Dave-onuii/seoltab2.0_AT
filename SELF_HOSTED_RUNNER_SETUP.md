# Self-Hosted Runner 설정 가이드

Self-Hosted Runner를 설정하면 **본인의 PC에서 GitHub Actions를 실행**할 수 있으며, **PC에 연결된 실제 디바이스**를 테스트할 수 있습니다.

---

## 목차
1. [Self-Hosted Runner란?](#self-hosted-runner란)
2. [설정 방법](#설정-방법)
3. [Runner 실행](#runner-실행)
4. [워크플로우 수정](#워크플로우-수정)
5. [테스트 실행](#테스트-실행)
6. [문제 해결](#문제-해결)

---

## Self-Hosted Runner란?

### GitHub Actions의 두 가지 실행 방식

| 구분 | GitHub-Hosted Runner | Self-Hosted Runner |
|------|----------------------|---------------------|
| **실행 위치** | GitHub 클라우드 서버 | 본인의 PC/서버 |
| **디바이스 접근** | 불가능 | **가능 (PC에 연결된 디바이스)** |
| **비용** | 무료 (제한 있음) | 무료 (PC 리소스 사용) |
| **설정** | 간단 | 초기 설정 필요 |
| **실행 조건** | 항상 가능 | **PC가 켜져 있어야 함** |

---

## 설정 방법

### 1. GitHub 저장소에서 Runner 등록

1. **GitHub 저장소 접속**: `https://github.com/dave-onuii/seoltab2.0_AT`

2. **Settings > Actions > Runners 이동**:
   ```
   Settings 탭 클릭
   → 좌측 메뉴에서 "Actions" 클릭
   → "Runners" 클릭
   → "New self-hosted runner" 클릭
   ```

3. **Runner 설정 선택**:
   - **Runner image**: `macOS` 선택 (본인 PC가 macOS이므로)
   - **Architecture**: `ARM64` 또는 `x64` (Mac의 칩 종류에 따라)
     - **M1/M2/M3 Mac**: `ARM64`
     - **Intel Mac**: `x64`

4. **다운로드 및 설정 명령어 복사**:
   GitHub에서 제공하는 명령어가 표시됩니다. 아래와 비슷한 형태입니다:

---

### 2. 본인의 Mac에서 Runner 설치

터미널을 열고 아래 명령어를 실행합니다:

#### Step 1: Runner 디렉토리 생성 및 이동
```bash
mkdir -p ~/actions-runner && cd ~/actions-runner
```

#### Step 2: Runner 다운로드
```bash
# M1/M2/M3 Mac (ARM64)
curl -o actions-runner-osx-arm64-2.313.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.313.0/actions-runner-osx-arm64-2.313.0.tar.gz

# 또는 Intel Mac (x64)
# curl -o actions-runner-osx-x64-2.313.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.313.0/actions-runner-osx-x64-2.313.0.tar.gz
```

#### Step 3: 압축 해제
```bash
# M1/M2/M3 Mac
tar xzf ./actions-runner-osx-arm64-2.313.0.tar.gz

# Intel Mac
# tar xzf ./actions-runner-osx-x64-2.313.0.tar.gz
```

#### Step 4: Runner 등록 (중요!)
```bash
./config.sh --url https://github.com/dave-onuii/seoltab2.0_AT --token YOUR_TOKEN_HERE
```

**주의**: `YOUR_TOKEN_HERE` 부분은 GitHub에서 제공한 실제 토큰으로 교체해야 합니다.

설정 중 질문에 답변:
```
Enter the name of the runner group: [press Enter for Default]
→ 그냥 Enter (기본값 사용)

Enter the name of runner: [press Enter for 본인PC이름]
→ 그냥 Enter 또는 원하는 이름 입력 (예: mac-runner)

Enter any additional labels: [press Enter to skip]
→ 그냥 Enter (추가 레이블 불필요)

Enter name of work folder: [press Enter for _work]
→ 그냥 Enter (기본값 사용)
```

---

## Runner 실행

### 방법 1: 수동 실행 (테스트용)
```bash
cd ~/actions-runner
./run.sh
```
- 터미널을 닫으면 Runner가 종료됩니다.
- 테스트할 때 사용하세요.

### 방법 2: 백그라운드 서비스로 실행 (권장)
```bash
cd ~/actions-runner
sudo ./svc.sh install
sudo ./svc.sh start
```

**장점**:
- Mac을 재부팅해도 자동으로 실행됩니다.
- 터미널을 닫아도 계속 실행됩니다.

**서비스 제어 명령어**:
```bash
# 상태 확인
sudo ./svc.sh status

# 중지
sudo ./svc.sh stop

# 재시작
sudo ./svc.sh restart

# 제거
sudo ./svc.sh uninstall
```

---

## 워크플로우 수정

Self-Hosted Runner를 사용하려면 워크플로우 파일을 수정해야 합니다.

### 기존 (GitHub-Hosted Runner)
```yaml
jobs:
  test:
    runs-on: ubuntu-latest  # GitHub 클라우드 서버
```

### 수정 후 (Self-Hosted Runner)
```yaml
jobs:
  test:
    runs-on: self-hosted  # 본인의 Mac
```

---

## 테스트 실행

### 1. 로컬에서 Appium Server 실행
```bash
appium
```

### 2. GitHub에서 워크플로우 실행
1. **Actions 탭 이동**
2. **워크플로우 선택** (예: "Device Test with Self-Hosted Runner")
3. **Run workflow 클릭**
4. **브랜치 선택** → **Run workflow**

### 3. 실행 확인
- Runner가 실행 중인 터미널에서 로그 확인
- GitHub Actions 페이지에서 실행 상태 확인
- PC에 연결된 디바이스에서 테스트 실행 확인

---

## 문제 해결

### 1. Runner가 GitHub에 연결되지 않음
**증상**: Actions에서 워크플로우가 대기 상태 ("Queued")

**해결**:
```bash
cd ~/actions-runner
./run.sh  # Runner가 정상 실행되는지 확인
```

터미널에 `Listening for Jobs` 메시지가 표시되면 정상입니다.

---

### 2. Appium 연결 실패
**증상**: `Could not connect to Appium server`

**해결**:
1. **Appium Server가 실행 중인지 확인**:
   ```bash
   ps aux | grep appium
   ```

2. **Appium Server 실행**:
   ```bash
   appium
   ```

3. **워크플로우에서 Appium을 자동 시작하도록 설정** (선택적):
   ```yaml
   - name: Start Appium Server
     run: |
       appium &
       sleep 5
   ```

---

### 3. 디바이스가 인식되지 않음
**증상**: `Device not found`

**해결**:
1. **디바이스 연결 확인**:
   ```bash
   # Android
   adb devices

   # iOS
   xcrun xctrace list devices
   ```

2. **Runner 실행 사용자 확인**:
   - Service로 실행 시 권한 문제가 발생할 수 있습니다.
   - 테스트용으로 `./run.sh`로 직접 실행해보세요.

---

### 4. Runner가 자동으로 종료됨
**증상**: 일정 시간 후 Runner가 꺼짐

**해결**:
- **Service로 설치** (위의 "방법 2" 참조)
- Mac의 절전 모드 설정 확인

---

### 5. 권한 오류 (Permission Denied)
**증상**: `Permission denied` 오류 발생

**해결**:
```bash
cd ~/actions-runner
chmod +x config.sh run.sh svc.sh
```

---

## 추가 정보

### Runner 제거 방법
```bash
cd ~/actions-runner

# 서비스 중지 및 제거
sudo ./svc.sh stop
sudo ./svc.sh uninstall

# GitHub에서 Runner 등록 해제
./config.sh remove --token YOUR_TOKEN_HERE

# 디렉토리 삭제
cd ~
rm -rf actions-runner
```

---

### 보안 고려사항
- Self-Hosted Runner는 **본인의 PC 리소스를 사용**합니다.
- **Public 저장소에서는 주의**: 누구나 워크플로우를 실행할 수 있습니다.
- **Private 저장소 권장**: 팀원만 접근 가능하도록 설정하세요.

---

### 참고 자료
- [GitHub Actions - Self-Hosted Runners 공식 문서](https://docs.github.com/en/actions/hosting-your-own-runners/about-self-hosted-runners)
- [Appium 공식 문서](http://appium.io/docs/en/latest/)
