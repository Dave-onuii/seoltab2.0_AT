#!/bin/bash
# Allure 리포트 생성 및 열기 스크립트

echo "================================"
echo "Allure 리포트 생성 중..."
echo "================================"

# Allure 리포트 생성
allure generate allure-results --clean -o allure-report

if [ $? -eq 0 ]; then
    echo ""
    echo "================================"
    echo "✅ 리포트 생성 완료!"
    echo "================================"
    echo ""
    echo "리포트를 브라우저에서 여는 중..."

    # Allure 리포트 열기
    allure open allure-report
else
    echo ""
    echo "================================"
    echo "❌ 리포트 생성 실패"
    echo "================================"
    exit 1
fi
