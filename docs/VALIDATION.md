# 검증 결과와 준비 상태

## 2026년 10월 30일 시작 프로필 추가 검증

- 시작 프로필 8개 문서 생성, 기본값 네트워크 미사용, 기존 폴더 덮어쓰기·경로 이탈 거부, fetch 커밋 기록 검사를 추가했습니다.
- 전체 35개 테스트와 기존 4개 합성 예제가 통과했습니다. 분류 기준선은 기존과 같은 12건 중 11건입니다.
- `prepare web launchpad-fetch-check --fetch`로 FastAPI Template을 실제 clone했고 `f4bcfaba7c85be3c6332cc74a20819f586dcdbc6`을 기록했습니다. 외부 앱 설치·실행 검증은 아닙니다.
- Docker 실행 파일이 없어 `.devcontainer` 설정은 작성·JSON 확인까지만 했습니다.
- 예전 오프라인 ZIP은 이번 변경을 포함하지 않습니다. 이번 소스 ZIP 또는 Git 저장소에서 최신 소스를 가져오세요.

아래는 이전 실행·브라우저·오프라인 번들의 검증 기록입니다.

기준일: 2026-10-26 KST. Windows x64 / Python 3.13.5. 초기 문서 전용 키트의 6개 테스트에서 실행 키트 검증으로 확장했다.

## 실제 통과한 검증

| 범위 | 결과 | 증거 |
|---|---|---|
| 현재 소스 자동 테스트 | 32개 통과 | [tests.log](../evidence/runtime/tests.log) |
| 소스 해시·미검증 경계 | 검증 시점 코드와 함께 기록 | [verification.json](../evidence/runtime/verification.json) |
| 새 프로젝트 오프라인 설치 | 새 .venv에 저장된 wheel 55개로 설치, pip check 통과 | [설치 로그](../evidence/runtime/offline-install.log) |
| 오프라인 복사본 실행 | 당시 소스의 테스트 29개와 예제 실행 통과 | [복사본 테스트](../evidence/runtime/offline-tests.log) |
| ZIP 복구 후 실행 | 159개 파일의 해시 검증·새 폴더 복구·테스트 32개 통과 | [복구 검증](../evidence/runtime/portable-validation.json) |
| 최종 오프라인 번들 | 221개 파일 복구, 번들 내부 wheel만으로 새 가상환경 설치, 32개 테스트·4개 예제 통과, 현재 소스 해시 일치 | [번들 검증](../evidence/runtime/bundle-validation.json), [설치](../evidence/runtime/bundle-install.log), [테스트](../evidence/runtime/bundle-tests.log) |
| 실제 HTTP API | CLI에서 구매 요청 접수·승인·로컬 기록 완료 | [http-smoke.json](../evidence/runtime/http-smoke.json) |
| 브라우저 사용자 흐름 | 시설 요청 접수·승인·기록, 재시작 후 조회, CLI 결과 웹 조회 | [최종 화면](../evidence/runtime/workbench-final.png) |
| 반응형 웹 | 390px viewport에서 문서 너비 375px, 가로 넘침 없음 | [화면](../evidence/runtime/workbench-mobile.png) |
| DB 백업 | SQLite online backup·integrity_check 통과, 테스트에서 복구 상태 조회 | backups/data-*.sqlite3 |
| 공식 레포 조사 | 28개 README·메타데이터·루트 라이선스 저장 | [후보 목록](REPOSITORIES.md) |

32개 테스트는 모든 도메인의 정확성이나 보안을 증명하는 숫자가 아니다. 승인·버전·해시·권한·동시 실행·입력 경계·재시작·복구·모델 대안·예제 계산 등 구체적인 조건을 검사한다.

## 문제별 실제 결과

[capabilities.json](../evidence/runtime/capabilities.json)에 실행 결과를 저장했다.

- 문서: alpha 작업공간의 환불 문서를 찾고 beta 문서는 제외. 근거 없는 검색은 abstained. 합성 텍스트 변환과 키워드 검색이며 PDF/OCR/RAG 품질은 미검증.
- 표 분석: 합성 주문 4건의 총액 133,000원. books 42,000원, equipment 91,000원으로 손계산과 일치.
- 일정: 3명·3슬롯에서 선호 3개를 충족하는 OPTIMAL 결과. 한 슬롯에 두 명을 강제하면 INFEASIBLE. 실시간 예약 시스템은 아님.
- 추천: 태그 일치·인기도 기준으로 후보를 제시하고 종료/제외 항목을 제거. 학습 모델이 아닌 cold-start 기준선.

## 분류 평가에서 드러난 한계

[baseline-evaluation.json](../evidence/runtime/baseline-evaluation.json)의 합성 12건에서 **기대 분류 11건 일치**. s11은 환불 요청 뒤의 지시문에 결제 키워드가 섞여 unknown으로 보류했다. 키워드 기준선의 실제 한계이며 실제 LLM 정확도가 아니다.

이 평가는 category만 비교한다. fixture의 expected_action 전체, 주문 번호 누락 처리, 현업의 업무 적합성까지 통과했다고 표시하지 않는다. 실제 모델은 Pydantic AI TestModel로 호출 형식과 오류 대안만 검증했다.

## 아직 실제로 검증하지 않은 경계

- 외부 유료/로컬 LLM의 언어 이해·비용·지연·실제 장애.
- 공개 서비스의 사용자 인증·운영 배포·외부 이메일/결제/주문 원장.
- 음성·시각 모델, Expo/Flutter 네이티브 앱, 실기기 권한.
- Linux/macOS 설치와 다른 Python 버전.
- 도메인 재사용률 80% 또는 Probe 평가 점수.

위 항목은 [추가 구성](OPTIONAL_PROFILES.md)과 [실행 안내](RUNBOOK.md)의 도입 조건을 따라 별도로 검증한다. 사용자 제공 평가 설명의 기술·의도·인지 100점과 소통 배점 미상은 공식 공고를 확인한 점수표가 아니다.

## 확인 과정에서 수정한 문제

2026-10-26 디자인 라이브러리 추가 후에도 32개 테스트가 통과했다. 테마 12종·캡처 24장 원본 해시와 갤러리 로컬 링크를 확인했고, 새 `work/design-ready` 프로젝트에 디자인 폴더가 동일하게 복사되는지 검사했다. 브라우저에서 예약 검색 1건, 업무 분류 4건, 밝음/어두움 전환·이미지 로딩·프롬프트 복사 성공을 확인했다. 1280px에서 3열, 390px에서 콘텐츠 폭과 스크롤 폭 모두 375px로 가로 넘침이 없었다. [디자인 검증 기록](../evidence/runtime/design-library-validation.json). 이전 오프라인 번들 검증은 그 당시 소스의 기록이며 신규 디자인 폴더와 수정된 kit.py를 포함하지 않는다.

Windows 임시 폴더 ACL 문제는 프로젝트 임시 경로로 해결했다. Pydantic AI 2.61.0의 usage 속성 차이는 실제 SDK 테스트로 발견·수정했다. 브라우저 접근은 loopback 서버를 일반 로컬 실행에서 확인했다. 자세한 선택 이유는 [결정 기록](DECISIONS.md)에 있다.

