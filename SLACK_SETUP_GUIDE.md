# Slack 알림 설정 가이드

Allure 리포트 생성 시 Slack 채널에 자동으로 알림을 보내는 기능 설정 가이드입니다.

---

## 📋 목차

1. [Slack Webhook URL 생성](#1-slack-webhook-url-생성)
2. [로컬 환경 설정](#2-로컬-환경-설정)
3. [GitHub Actions 설정](#3-github-actions-설정)
4. [사용 방법](#4-사용-방법)
5. [문제 해결](#5-문제-해결)

---

## 1. Slack Webhook URL 생성

### Step 1: Slack App 만들기

1. **Slack API 페이지 접속**
   - https://api.slack.com/apps 접속
   - "Create New App" 클릭

2. **"From scratch" 선택**
   - App Name: `Test Automation Reporter` (원하는 이름)
   - Workspace: 알림을 받을 워크스페이스 선택
   - "Create App" 클릭

### Step 2: Incoming Webhooks 활성화

1. **Incoming Webhooks 활성화**
   - 왼쪽 메뉴에서 "Incoming Webhooks" 클릭
   - "Activate Incoming Webhooks" 토글을 ON으로 변경

2. **Webhook URL 생성**
   - 하단의 "Add New Webhook to Workspace" 클릭
   - 알림을 받을 채널 선택 (예: `#test-automation`, `#dev-alerts`)
   - "Allow" 클릭

3. **Webhook URL 복사**
   - 생성된 Webhook URL 복사
   - 형식: `https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXX`
   - ⚠️ **이 URL은 외부에 노출되면 안 됩니다!**

---

## 2. 로컬 환경 설정

### 방법 A: 환경 변수 설정 (권장)

#### macOS/Linux

```bash
# ~/.zshrc 또는 ~/.bashrc에 추가
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

# 적용
source ~/.zshrc  # 또는 source ~/.bashrc
```

#### 임시로 사용 (한 번만)

```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
pytest --auto-report --slack
```

### 방법 B: .env 파일 사용 (선택사항)

1. **.env 파일 생성** (프로젝트 루트)

```bash
# .env
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

2. **.gitignore에 추가** (이미 추가되어 있음)

```
.env
```

3. **python-dotenv 설치** (선택사항)

```bash
pip install python-dotenv
```

---

## 3. GitHub Actions 설정

### Step 1: GitHub Repository Secrets 등록

1. **GitHub 저장소 페이지 접속**
   - https://github.com/Dave-onuii/seoltab2.0_AT

2. **Settings > Secrets and variables > Actions 이동**

3. **New repository secret 클릭**
   - Name: `SLACK_WEBHOOK_URL`
   - Secret: 복사한 Webhook URL 붙여넣기
   - "Add secret" 클릭

### Step 2: GitHub Pages 활성화

1. **Settings > Pages 이동**

2. **Source 설정**
   - Source: "Deploy from a branch" 선택
   - Branch: `gh-pages` 선택, `/ (root)` 선택
   - "Save" 클릭

3. **확인**
   - 몇 분 후 "Your site is published at https://dave-onuii.github.io/seoltab2.0_AT/" 메시지 확인

---

## 4. 사용 방법

### 로컬에서 사용

#### 기본 사용 (Slack 알림 없음)
```bash
pytest
```

#### 리포트만 생성 (Slack 알림 없음)
```bash
pytest --auto-report
```

#### 리포트 생성 + Slack 알림
```bash
pytest --auto-report --slack
```

#### 특정 테스트 + 리포트 + Slack
```bash
pytest tests/test_dummy.py --auto-report --slack
```

### Slack 알림 메시지 예시

로컬 실행 시:
```
✅ 테스트 통과: Allure 리포트가 생성되었습니다!

테스트 결과
✅ Passed: 5
❌ Failed: 0
⏭️ Skipped: 1
📊 Total: 6

실행 정보
⏱️ Duration: 1.5s
🌍 Environment: 로컬
🌿 Branch: main

📊 Allure 리포트
file:///Users/davekim/seoltab_AT/allure-report/index.html

Commit: abc1234
```

GitHub Actions 실행 시:
```
✅ GitHub Actions: Allure 리포트가 생성되었습니다!

실행 정보
🌿 Branch: main
👤 Actor: Dave-onuii
🔢 Run: #42

📊 Allure 리포트
리포트 보기 (클릭 가능한 링크)
https://dave-onuii.github.io/seoltab2.0_AT/reports/42/index.html

Commit: abc1234
```

---

## 5. 문제 해결

### ❌ "SLACK_WEBHOOK_URL 환경 변수가 설정되지 않았습니다"

**원인**: 환경 변수가 설정되지 않음

**해결**:
```bash
# 환경 변수 설정 확인
echo $SLACK_WEBHOOK_URL

# 설정
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."

# 다시 실행
pytest --auto-report --slack
```

### ❌ "Slack 알림 전송 실패"

**원인 1**: Webhook URL이 잘못됨

**해결**: Webhook URL을 다시 확인하고 복사

**원인 2**: 네트워크 문제

**해결**:
```bash
# curl로 직접 테스트
curl -X POST "$SLACK_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{"text":"테스트 메시지"}'

# 응답: "ok"가 나와야 정상
```

### ⚠️ "--slack 옵션은 --auto-report와 함께 사용해야 합니다"

**원인**: `--slack`만 단독으로 사용

**해결**:
```bash
# 잘못된 사용
pytest --slack  # ❌

# 올바른 사용
pytest --auto-report --slack  # ✅
```

### ❌ GitHub Actions에서 Slack 알림이 안 옴

**원인**: GitHub Secret이 설정되지 않음

**해결**:
1. GitHub > Settings > Secrets and variables > Actions
2. `SLACK_WEBHOOK_URL` Secret이 있는지 확인
3. 없으면 추가

---

## 📚 추가 정보

### Slack 메시지 커스터마이징

`utils/slack_notifier.py` 파일을 수정하여 메시지 형식을 변경할 수 있습니다.

### GitHub Pages 리포트 히스토리

- 각 실행마다 별도 디렉토리에 저장: `/reports/1/`, `/reports/2/`, ...
- 최대 30일간 보관 (설정 변경 가능)
- 최신 리포트: https://dave-onuii.github.io/seoltab2.0_AT/reports/latest/

### 알림 채널 변경

1. Slack API 페이지에서 기존 Webhook 삭제
2. 새 채널에 대한 Webhook 생성
3. 환경 변수 업데이트

---

## 🎉 완료!

이제 테스트를 실행하면 자동으로 Slack 채널에 알림이 전송됩니다!

```bash
pytest --auto-report --slack
```
