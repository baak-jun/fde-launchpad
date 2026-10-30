# 범용 FDE 키트 인수인계

## 2026년 10월 30일 시작 기반 구성

- `python kit.py choose`, `prepare <profile> <name> [--fetch]` 추가. 8개 프로필은 catalog/launchpads.json.
- local은 기존 실행 소스 복사, 나머지는 시작 안내·작업 문서 생성. fetch는 공식 Git clone 후 커밋 기록만 하며 설치·실행하지 않음.
- docs/START_BY_PROBLEM.md와 REPOSITORY_MAP.md가 새 진입점.
- `.devcontainer`는 Python 3.13 Linux 환경 설정 초안. Docker 빌드·Linux 설치는 아직 검증하지 않음.
- GitHub 정리 저장소 이름: fde-launchpad. 샌드박스 내부 gh 인증 오류는 외부 keyring 접근으로 해소됨. 원격 생성·업로드 결과는 git remote와 GitHub URL로 확인할 것.

## 사용자 목표

특정 해커톤에 종속하지 않는 재사용 키트. 인증·레이아웃을 넘어 업무 처리에 쓸 GitHub 베이스와 실행 준비물을 갖추고, 앞으로 바로 복사해 시작할 수 있게 한다. 사용자가 제공한 AI Native 기준(기술·의도·인지·소통)에 맞춰 이해하기 쉬운 설명과 과정·검증 증거를 남긴다. 전체 개선 전후에 복구 가능한 백업을 유지한다.

## 읽는 순서

README.md → docs/HOW_IT_WORKS.md → docs/AI_NATIVE.md → docs/VALIDATION.md → docs/RUNBOOK.md.

## 구현된 것

- 디자인 v2: index.html은 getdesign.kr의 한국 8종 화면 발췌 + getdesign.md 공개 MD 기반 해외 신규 시안 4종을 보여준다. 기존 12종은 token-gallery.html에 보존. 총 24종. 원본/발췌/신규 시안과 자리표시자 한계는 design-library/SHOWCASE.md에 명시. build_design_showcase.py가 새 갤러리를 생성하고 기존 build_design_library.py는 v2 존재 시 token-gallery.html만 생성한다. 현재 앱에 특정 테마를 적용한 것은 아니다.

- design-library/index.html: 검색·분류·라이트/다크 비교가 가능한 로컬 디자인 갤러리. 원본 DESIGN.md 12종, 저장소 제공 예시 캡처 24장, 한국어 적용 권고·프롬프트·출처 해시. 실제 브랜드 화면이나 공식 가이드가 아님. 특정 테마를 업무 실험실에 아직 적용하지 않았다. kit.py start로 함께 복사된다. 이전 FDE 오프라인 ZIP에는 신규 디자인 폴더가 없다.

- FastAPI/Pydantic AI/SQLite를 연결한 로컬 업무 실험실. 접수·초안·수정·승인/거부·로컬 기록·이력.
- 고객 문의·시설·구매 도메인 팩. 작업공간별 조회, 역할별 변경 권한, 버전·해시 검사, SQLite 트랜잭션 기반 중복 방지.
- MarkItDown 키워드 검색, DuckDB 고정 집계, OR-Tools 배정, 규칙 추천 기준선.
- kit.py recipes/find/new/start/demo. start는 독립 소스를 복사하고 같은 이름을 거부한다.
- 고정 의존성, 설치·진단·검증·소스/DB 백업·wheel 캐시 스크립트.
- 28개 후보·8개 레시피, 작업 의도·이해도·인수인계 템플릿.
- skills/fde-workbench-flow/SKILL.md: 키트 전용 재개·도메인 변경·검증·인수인계 절차. 전역 설치는 하지 않았으며 파일 경로로 읽어 사용한다. skill-creator의 quick_validate 통과.

## 검증의 기준 파일

- evidence/runtime/tests.log: 실제 테스트 목록과 결과.
- evidence/runtime/verification.json: 검증 시각·소스 해시·외부/장치 미검증 플래그.
- evidence/runtime/capabilities.json: 4개 예제 결과.
- evidence/runtime/baseline-evaluation.json: 규칙 분류 12건 중 11건 일치, s11 보류. 모델 정확도 아님.
- evidence/runtime/workbench-desktop.png, workbench-mobile.png: 브라우저 확인 화면.
- evidence/runtime/offline-install.log: 새 프로젝트 오프라인 설치 로그. 최종 성공과 별도 재검증 결과를 함께 확인할 것.
- evidence/runtime/bundle-validation.json: 최종 오프라인 ZIP을 새 폴더에 복구하고 내부 wheel만으로 설치. 32개 테스트·4개 예제 실행, 원본과 검증 대상 소스 해시 일치. 설치 로그는 bundle-install.log, 테스트는 bundle-tests.log.

## 준비 완료 후 첫 사용

준비 키트 v1은 로컬 실행·복사·오프라인 복구까지 확인했다. README와 docs/QUICKSTART_15MIN.md부터 읽고 `python kit.py start my-project`로 별도 프로젝트를 만든다. 실제 문제의 목표·제약을 채우고 도메인 팩을 수정한 다음, 실제 데이터와 선택한 모델로 새 평가를 수행한다. 현재 번들은 Windows x64 / Python 3.13용이며 최신 검증 문서와 DB 백업은 작업 폴더와 최종 소스 체크포인트에도 보존한다.

## 실행과 재개

```powershell
.venv/Scripts/python.exe scripts/doctor.py
.venv/Scripts/python.exe scripts/verify.py
.venv/Scripts/python.exe run_workbench.py
```

주요 URL은 http://127.0.0.1:8765 . 기존 서버가 있는지 먼저 health를 확인한다. 지난 프로세스 번호를 현재 liveness로 간주하지 않는다. 모델 모드는 기본 rules이며 FDE_ENABLE_LIVE=1을 명시했을 때만 외부 모델을 구성한다. 키는 기록하지 않는다.

## 다음 변경 전

1. 사용자 수정과 Git 상태를 확인한다. 초기 Git은 커밋이 없었고 이 작업은 ZIP 백업을 사용했다.
2. checkpoint로 소스를, backup_data로 DB를 보존한다. work/의 복사 프로젝트는 각 폴더에서 백업한다.
3. 변경할 목표·파일·검증을 INTENT 양식에 정한다.
4. 확인되지 않은 모델 품질·외부 원장·장치·배포를 이미 완료된 것으로 표시하지 않는다.

## 알려진 한계

기본 UI는 로컬 운영자 데모이며 공개 서비스용 인증이 아니다. 외부 이메일·결제·원장 연결은 없다. Pydantic AI TestModel만 호출 검증했고 실제 유료 LLM은 호출하지 않았다. 문서 예제는 텍스트/키워드 기준선이다. 음성·이미지·커머스 전체 제품과 네이티브 장치는 조건별 추가 구성이다. 이 한계를 지운 채 결과를 인계하지 않는다.
