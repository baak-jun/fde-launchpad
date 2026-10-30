# 범용 FDE 준비 키트

## 문제에 맞는 기반부터 고르기

**[문제 유형별 시작 가이드](docs/START_BY_PROBLEM.md)**에서 실행 방법과 선택 기준을 확인하세요. 비공개 GitHub 저장소는 [baak-jun/fde-launchpad](https://github.com/baak-jun/fde-launchpad)입니다.

[상황별 외부 저장소 지도](docs/REPOSITORY_MAP.md)에서 앱 기반·AI·문서·모바일·커머스 후보를 고를 수 있습니다.

```powershell
python kit.py choose
python kit.py prepare local my-demo
python kit.py prepare web my-service --fetch
```

`local`은 현재 실행 앱을 복사합니다. `web`, `admin`, `business`, `ai`, `internal`, `dyad`, `bolt`는 외부 기반의 시작 문서를 만들고, `--fetch`를 붙이면 공식 원본도 가져옵니다. 외부 앱 설치·통합은 생성된 `START_HERE.md`를 따르세요.

문제에 맞는 오픈소스를 고르고, 실행해 보고, 새 프로젝트로 복사해 시작하는 키트입니다. **업무 실험실 + 실행 예제 + GitHub 후보 28개 + AI 작업·설명·인수인계 체계**가 들어 있습니다. 모든 산업 문제의 80%가 완성된 제품이라는 뜻은 아닙니다.

## 먼저 실행해 보기

이 컴퓨터에는 실행 환경을 준비했습니다. `launch.cmd`를 열거나 아래 명령을 실행하고 [업무 실험실](http://127.0.0.1:8765)을 여세요. 이미 서버가 실행 중이면 기존 화면을 사용하세요. 종료는 터미널에서 Ctrl+C입니다.

```powershell
.venv/Scripts/python.exe run_workbench.py
```

시설 요청·구매 요청·고객 문의 중 하나 선택 → **예제 넣기 → 검토 초안 만들기 → 승인 → 로컬 기록 생성**. 승인 후 입력을 수정하면 승인이 해제됩니다.

기본 분류는 **규칙 기반**, 실행은 **이 기기의 DB 기록**입니다. 실제 모델 호출·발송·결제는 기본적으로 하지 않습니다. 로컬 화면의 운영자 권한은 공개 서비스용 로그인을 대체하지 않습니다.

## 무엇이 준비됐나

| 준비물 | 할 수 있는 것 |
|---|---|
| 업무 실험실 | 접수·분류·근거·수정·승인/거부·중복 방지·기록·재시작 |
| 도메인 팩 3개 | 고객 문의·시설 요청·구매 요청을 같은 코드로 실행 |
| 실행 예제 4개 | 문서 키워드 검색, SQL 집계, 제약 기반 일정 배정, 추천 기준선 |
| Pydantic AI 어댑터 | 구조화 응답·테스트 모델 경로 검증; 외부 실모델 연결은 별도 |
| [후보 28개](docs/REPOSITORIES.md)와 [조합 8개](docs/RECIPES.md) | 문제별 GitHub·사용 시점·라이선스·주의점 확인 |
| 새 프로젝트 생성 | 소스·잠금 파일·작업 양식 복사; 키·DB·가상환경은 제외 |
| [AI Native 4축 체계](docs/AI_NATIVE.md) | 목표·제약·검증·구조 이해·인수인계 준비 |
| 백업·복구·오프라인 설치 | 소스 ZIP, DB 온라인 백업, 같은 환경용 wheel 캐시 |

기능별 증거는 [검증 기록](docs/VALIDATION.md)에 있습니다. 음성·이미지·커머스·네이티브 앱은 [추가 구성](docs/OPTIONAL_PROFILES.md)의 조건을 확인하세요.

## 바로 가져다 쓰기

다른 같은 환경의 PC로 가져갈 때는 `backups/*-fde-offline-windows-py313.zip` 번들을 사용합니다. Python 3.13이 설치된 Windows x64에서 새 폴더에 풀고 `./scripts/setup.ps1 -Offline`을 실행하세요. Python 자체·모델·키·DB는 포함하지 않습니다.

```powershell
# 실행 가능한 소스와 인수인계 자료 복사
python kit.py start my-project
# 계획 문서만 만들기
python kit.py new analytics my-analysis-plan
# 문제 유형과 레포 검색
python kit.py recipes
python kit.py find document
```

`work/my-project/`에 독립적인 소스가 생깁니다. 같은 이름은 덮어쓰지 않습니다. 복사된 evidence는 원본 키트 기록이므로 새 환경에서 다시 검증하세요.

```powershell
cd work/my-project
./scripts/setup.ps1
.venv/Scripts/python.exe scripts/verify.py
.venv/Scripts/python.exe run_workbench.py --port 8766
```

`BRIEF.md`에 실제 문제, `INTENT.md`에 목표와 제약을 채우고 `domain_packs/`를 수정합니다. `UNDERSTANDING.md`로 직접 설명해 보고 마지막 상태는 `HANDOFF.md`에 남깁니다.

## 문제별 예제

```powershell
.venv/Scripts/python.exe kit.py demo documents
.venv/Scripts/python.exe kit.py demo analytics
.venv/Scripts/python.exe kit.py demo planner
.venv/Scripts/python.exe kit.py demo recommendation
```

문서는 MarkItDown 변환과 키워드 검색, 분석은 DuckDB 고정 SQL, 일정은 OR-Tools, 추천은 태그·인기도 기준선입니다. 의미 검색/RAG 전체·실시간 예약 원장·학습 추천 모델을 구현했다는 뜻은 아닙니다.

## 읽는 순서

디자인을 고를 때는 [화면 중심 스크린샷 갤러리](design-library/index.html)를 여세요. getdesign.kr·getdesign.md에서 찾은 한국 8종·해외 4종을 기존 12종에 추가해 총 24종을 보관합니다. 원본 MD, 화면 캡처, 적용 안내와 프롬프트가 준비되어 있습니다. [v2 출처·적용 안내](design-library/SHOWCASE.md).

처음이라면 [15분 체험 안내](docs/QUICKSTART_15MIN.md)부터 읽으세요.

1. [무엇을 어떻게 만들었나](docs/HOW_IT_WORKS.md): 입력의 이동 경로, 바꿀 파일, 실패 지점.
2. [AI Native 준비](docs/AI_NATIVE.md): 기술·의도·인지·소통을 실제 작업에 연결.
3. [실행·모델·복구 안내](docs/RUNBOOK.md): 설치, 모델 설정, 상태 확인, 백업.
4. [결정 기록](docs/DECISIONS.md): 선택 이유와 실제 발견한 오류.
5. [인수인계](HANDOFF.md): 현재 상태와 다음 작업.

## 환경과 검증

다음 AI 세션에는 `skills/fde-workbench-flow/SKILL.md를 읽고 이 프로젝트를 이어서 작업해줘`라고 요청할 수 있습니다. 이 스킬은 키트 안에 동봉되며 전역 자동 발견 위치에는 설치하지 않았습니다.

검증 환경은 **Windows x64 / Python 3.13.5**입니다. Linux/macOS와 네이티브 실기기는 별도 검증이 필요합니다. 준비 문서 CLI는 표준 라이브러리만으로 실행됩니다.

```powershell
.venv/Scripts/python.exe scripts/doctor.py
.venv/Scripts/python.exe scripts/verify.py
python scripts/checkpoint.py before-change
.venv/Scripts/python.exe scripts/backup_data.py
```

소스 ZIP은 `work/`, `runtime-data/`, `.venv/`, `.cache/`, `.git/`, `.env*`를 제외합니다. 새 프로젝트는 **그 프로젝트 폴더 안에서** checkpoint를 실행하세요. DB는 backup_data.py로 따로 백업합니다.

