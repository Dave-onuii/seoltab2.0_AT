"""
Slack 알림 유틸리티

Allure 리포트 생성 후 Slack 채널에 알림을 보냅니다.
"""
import os
import json
import subprocess
from datetime import datetime
from typing import Optional


def send_slack_notification(
    report_url: str,
    test_result: dict,
    webhook_url: Optional[str] = None
) -> bool:
    """
    Slack 채널에 Allure 리포트 알림을 보냅니다.

    Args:
        report_url: Allure 리포트 URL
        test_result: 테스트 결과 정보 (passed, failed, skipped, total, duration)
        webhook_url: Slack Webhook URL (None이면 환경 변수에서 읽음)

    Returns:
        bool: 성공 시 True, 실패 시 False
    """
    # Webhook URL 가져오기
    if webhook_url is None:
        webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    if not webhook_url:
        print("⚠️  SLACK_WEBHOOK_URL 환경 변수가 설정되지 않았습니다.")
        print("💡 Slack 알림을 사용하려면 환경 변수를 설정하세요:")
        print("   export SLACK_WEBHOOK_URL='https://hooks.slack.com/services/...'")
        return False

    # 테스트 결과 파싱
    passed = test_result.get("passed", 0)
    failed = test_result.get("failed", 0)
    skipped = test_result.get("skipped", 0)
    total = test_result.get("total", 0)
    duration = test_result.get("duration", 0)
    exit_status = test_result.get("exit_status", 0)

    # 성공/실패 판단
    if exit_status == 0:
        status_emoji = "✅"
        status_text = "테스트 통과"
        color = "good"  # 녹색
    else:
        status_emoji = "❌"
        status_text = "테스트 실패"
        color = "danger"  # 빨간색

    # 환경 정보
    env = test_result.get("environment", "로컬")
    branch = test_result.get("branch", "unknown")
    commit = test_result.get("commit", "N/A")

    # Slack 메시지 구성
    slack_message = {
        "text": f"{status_emoji} {status_text}: Allure 리포트가 생성되었습니다!",
        "attachments": [
            {
                "color": color,
                "fields": [
                    {
                        "title": "테스트 결과",
                        "value": (
                            f"✅ Passed: {passed}\n"
                            f"❌ Failed: {failed}\n"
                            f"⏭️  Skipped: {skipped}\n"
                            f"📊 Total: {total}"
                        ),
                        "short": True
                    },
                    {
                        "title": "실행 정보",
                        "value": (
                            f"⏱️  Duration: {duration:.1f}s\n"
                            f"🌍 Environment: {env}\n"
                            f"🌿 Branch: {branch}"
                        ),
                        "short": True
                    }
                ],
                "footer": "설탭 2.0 테스트 자동화",
                "footer_icon": "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png",
                "ts": int(datetime.now().timestamp())
            }
        ]
    }

    # 리포트 링크 추가 (공개 URL이 있는 경우만)
    if report_url:
        # 공개 URL: 클릭 가능한 링크
        slack_message["attachments"][0]["fields"].append({
            "title": "📊 Allure 리포트",
            "value": f"<{report_url}|🔗 리포트 보기 (클릭!)>",
            "short": False
        })
    else:
        # 로컬 환경: 리포트 URL 없이 안내 메시지만
        slack_message["attachments"][0]["fields"].append({
            "title": "📊 Allure 리포트",
            "value": (
                "✅ 로컬에서 리포트가 생성되었습니다.\n\n"
                "💡 리포트 확인 방법:\n"
                "`allure open allure-report`\n\n"
                "💡 공개 URL로 공유하려면 GitHub Actions를 사용하세요."
            ),
            "short": False
        })


    # Commit 정보가 있으면 추가
    if commit and commit != "N/A":
        slack_message["attachments"][0]["fields"].append({
            "title": "Commit",
            "value": f"`{commit[:7]}`",
            "short": False
        })

    # curl로 Slack에 전송
    try:
        result = subprocess.run(
            [
                "curl",
                "-X", "POST",
                "-H", "Content-Type: application/json",
                "-d", json.dumps(slack_message),
                webhook_url
            ],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0 and result.stdout.strip() == "ok":
            print(f"✅ Slack 알림 전송 성공!")
            return True
        else:
            print(f"❌ Slack 알림 전송 실패")
            if result.stderr:
                print(f"   에러: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print("⏱️  Slack 알림 전송 시간 초과 (10초)")
        return False
    except Exception as e:
        print(f"❌ Slack 알림 전송 중 오류 발생: {e}")
        return False


def get_git_info() -> dict:
    """
    현재 Git 브랜치 및 커밋 정보를 가져옵니다.

    Returns:
        dict: branch, commit 정보
    """
    info = {
        "branch": "unknown",
        "commit": "N/A"
    }

    try:
        # 현재 브랜치
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            info["branch"] = result.stdout.strip()

        # 현재 커밋 해시
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            info["commit"] = result.stdout.strip()

    except Exception:
        pass

    return info


def get_local_report_url() -> str:
    """
    로컬 리포트 URL을 생성합니다.

    Returns:
        str: 로컬 파일 경로 또는 안내 메시지
    """
    import os
    cwd = os.getcwd()
    return f"file://{cwd}/allure-report/index.html"


if __name__ == "__main__":
    # 테스트용
    print("Slack 알림 테스트")
    print("=" * 60)

    # 더미 테스트 결과
    test_result = {
        "passed": 10,
        "failed": 2,
        "skipped": 1,
        "total": 13,
        "duration": 45.5,
        "exit_status": 1,  # 실패
        "environment": "로컬",
        **get_git_info()
    }

    # 로컬 리포트 URL
    report_url = get_local_report_url()

    # Slack 알림 전송
    success = send_slack_notification(report_url, test_result)

    if success:
        print("\n✅ 테스트 완료!")
    else:
        print("\n❌ 테스트 실패 - Webhook URL을 확인하세요.")
