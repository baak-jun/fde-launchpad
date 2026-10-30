# 문제 유형별 시작 가이드

처음에는 `python kit.py choose`로 기반을 고릅니다. 승인 흐름을 빠르게 보여주려면 `local`, 일반 서비스를 만들려면 `web`, 업무 데이터 중심이면 `business`가 출발점입니다.

## 1. 기반 선택

| 문제 | 프로필 | 생성되는 준비물 |
|---|---|---|
| 고객 문의·시설·구매 승인 | local | 현재 실행 앱 전체와 작업 문서 |
| 자유로운 웹 서비스 | web | FastAPI Template 연결 안내와 작업 문서 |
| 관리 화면·대시보드 | admin | Refine 연결 안내와 작업 문서 |
| 재고·구매·고객 관리 | business | Frappe 연결 안내와 작업 문서 |
| 문서 검색·AI 워크플로 | ai | Dify 연결 안내와 작업 문서 |
| 기존 DB/API 운영 화면 | internal | Appsmith 연결 안내와 작업 문서 |
| 로컬 AI 앱 제작 | dyad | Dyad 설치·사용 안내와 작업 문서 |
| 브라우저 AI 앱 제작 | bolt | bolt.diy 설치·사용 안내와 작업 문서 |

외부 기반은 공식 저장소의 설치 방법을 따릅니다. 프로필 생성만으로 외부 앱이나 통합이 완성되지는 않습니다.

## 2. 프로젝트 만들기

키트 폴더에서 실행합니다. 이름은 영문 소문자·숫자·하이픈·밑줄을 사용하며, 같은 폴더는 덮어쓰지 않습니다.

```powershell
python kit.py choose
python kit.py prepare local my-demo
python kit.py prepare web my-service --fetch
```

`work/my-demo`에는 실행 가능한 소스가 복사됩니다. `work/my-service`에는 시작 안내와 작업 문서, `upstream`에는 공식 원본 코드가 들어갑니다. `--fetch`는 Git과 인터넷이 필요하며 코드를 가져오기만 합니다. 가져온 커밋은 `UPSTREAM_COMMIT.txt`에 기록합니다. 설치·모델 호출·배포는 실행하지 않습니다.

인터넷이 없으면 `--fetch` 없이 준비한 뒤 `START_HERE.md`의 clone 명령을 나중에 실행하세요. 가져오기가 실패해도 준비 문서는 남으므로 삭제하거나 덮어쓰지 말고 해당 폴더에서 상태를 확인하세요.

## 3. 실제 문제에 맞추기

1. 생성 폴더의 `START_HERE.md`를 읽고 기반 앱을 실행합니다.
2. `BRIEF.md`에 사용자·입력·원하는 결과를 적습니다. `INTENT.md`에 시간·비용·금지 동작·완료 기준을 적습니다.
3. 원본 키트의 [디자인 갤러리](../design-library/index.html)에서 하나를 고릅니다. 해당 `DESIGN.md`와 [공통 규칙](../design-library/COMMON_RULES.md)을 앱 작업 폴더에 복사합니다. 원본 출처·라이선스도 유지합니다.
4. 정상 처리, 권한 거부, 입력 수정, 오류와 재시도 사례를 직접 실행합니다. 실제로 확인한 결과만 `EVALUATION.json`에 기록합니다.
5. `UNDERSTANDING.md`로 구조를 설명하고 `HANDOFF.md`에 실행 명령·미완료·다음 작업을 남깁니다.

현재 키트의 승인 코드가 필요하면 `runtime/store.py`의 버전·승인 해시·중복 실행 방지 규칙을 참고합니다. 외부 시스템의 DB·사용자 권한에 맞춰 다시 구현하고 검증해야 합니다. 이메일·결제는 로컬 DB 기록과 달리 외부 서비스의 멱등 키와 재조정이 필요합니다.

## 4. 기능별 저장소 더 고르기

[기존 28개 후보](REPOSITORIES.md)와 [8개 문제 조합](RECIPES.md)은 그대로 유지합니다. 시작 기반은 이 문서에서 고르고, 기능은 기존 목록에서 더합니다.

```powershell
python kit.py find document
python kit.py recipes
python kit.py new planner scheduling-plan
```

`new`는 계획 문서만 만들고, `prepare local`은 현재 앱을 복사합니다. `prepare web --fetch` 같은 명령은 외부 원본까지 내려받습니다.

## 5. 다른 PC와 백업

현재 오프라인 번들은 Windows x64·Python 3.13용입니다. 이번 변경보다 오래된 번들에는 새 프로필이 없을 수 있으므로 번들 생성 시점을 확인하세요.

`.devcontainer/devcontainer.json`은 Linux 컨테이너에서 현재 Python 앱을 개발하기 위한 추가 설정입니다. VS Code Dev Containers와 Docker를 준비한 후 폴더를 컨테이너에서 다시 엽니다. 첫 생성은 인터넷이 필요합니다. 컨테이너 터미널에서 다음 명령을 실행합니다.

```sh
python -m venv /tmp/fde-venv
/tmp/fde-venv/bin/pip install -r requirements.in
/tmp/fde-venv/bin/python scripts/verify.py
/tmp/fde-venv/bin/python -m uvicorn runtime.app:configured_app --factory --host 0.0.0.0 --port 8765
```

위 실행은 컨테이너 내부용입니다. 포트 전달은 로컬로 유지하세요. 컨테이너 빌드·Linux 의존성 설치는 별도 검증이 필요합니다. Windows용 wheel 캐시를 Linux에서 사용하지 않습니다.

```powershell
python scripts/checkpoint.py my-milestone
```

이 백업은 원본 키트 소스용이며 `work/`와 DB를 제외합니다. 새 프로젝트는 그 프로젝트 안에서 제공된 백업 도구를 실행하거나 별도 Git 저장소로 관리하세요. 외부 프로필 폴더는 `git init` 후 문서와 앱 변경을 커밋하세요. `upstream`은 별도 Git 저장소이므로 해당 앱 변경도 그 안에서 별도로 커밋해야 합니다. 키·사용자 데이터는 커밋하지 않습니다.

## 저장소 구성

비공개 GitHub 저장소는 **[baak-jun/fde-launchpad](https://github.com/baak-jun/fde-launchpad)**입니다. 추천 기반 8개는 `catalog/launchpads.json`, 기존 기능 후보 28개는 `catalog/repos.json`에 있습니다. 타 프로젝트를 모두 포크하지 않고 공식 원본 링크와 필요할 때 가져오는 명령을 관리합니다. 따라서 원본의 라이선스와 업데이트 경로를 유지할 수 있습니다.

GitHub 생성과 업로드 여부는 실제 원격 저장소 링크로 확인합니다. 로컬 문서에 이름이 적혀 있는 것만으로 생성된 것은 아닙니다.
