# 실행과 복구 안내

## 설치와 시작

`python scripts/package_offline.py`는 소스와 lockfile에 맞는 wheel을 하나의 ZIP으로 묶고 모든 해시를 확인한다. 결과는 backups/*-fde-offline-windows-py313.zip이다. 같은 Windows x64/Python 3.13 환경의 새 폴더에 풀고 `./scripts/setup.ps1 -Offline`을 실행한다. Python 자체와 외부 모델 파일은 번들에 포함하지 않는다.

검증 환경은 Windows x64 / Python 3.13.5다. `./scripts/setup.ps1`은 프로젝트 `.venv`에 requirements.lock의 버전을 설치한다. 시스템 패키지는 변경하지 않는다. 다른 프로젝트의 가상환경을 복사하지 않는다.

서버는 `.venv/Scripts/python.exe run_workbench.py`로 시작한다. 주소는 http://127.0.0.1:8765 이며 포트 충돌이면 `--port 8766`을 붙인다. 기존 서버를 이유 없이 종료하지 않는다. 종료는 Ctrl+C다. sandbox 내부 서버가 외부 브라우저에서 보이지 않으면 일반 로컬 터미널에서 확인한다. 외부 공개 주소나 방화벽을 임의로 변경하지 않는다.

온라인 상태에서 `./scripts/cache_wheels.ps1`로 설치 파일을 저장한 뒤 `./scripts/setup.ps1 -Offline`을 사용할 수 있다. 캐시는 `.cache/wheels`이며 해당 OS·Python·아키텍처용이다. 다른 장치에 가져갈 때 소스 ZIP과 별도로 복사한다. 새 프로젝트는 원본 캐시 경로를 지정할 수 있다.

```powershell
./scripts/setup.ps1 -Offline -WheelDirectory ../../.cache/wheels
```

## API와 사용자 경계

API 설명은 `/api/docs`에 있다. 요청에는 Bearer 토큰이 필요하다. 기본 UI의 토큰은 로컬 운영자 연결용이며 계정 인증을 대체하지 않는다. 공개 서비스에는 검증된 OIDC/JWT 등으로 Principal을 만들고 작업공간·역할을 서버에서 결정해야 한다. 클라이언트가 보내는 tenant 값으로 권한을 부여하지 않는다. 로컬 접근 가능한 다른 사용자도 데모 화면을 사용할 수 있다.

## 실제 모델 연결

기본 rules 모드는 키와 외부 호출이 없다. 제공자 계정·데이터 전송 범위를 정한 뒤 환경 변수로 켠다. 키는 화면·문서·커밋에 넣지 않는다. `.env` 파일을 자동으로 읽는 기능은 없다.

```powershell
$env:FDE_ENABLE_LIVE='1'
$env:FDE_MODEL='openai:YOUR_MODEL_ID'
$env:FDE_DAILY_CALL_LIMIT='20'
# OPENAI_API_KEY는 본인 환경의 비밀값 관리 방식으로 설정
.venv/Scripts/python.exe run_workbench.py
```

모델 이름은 설정 형식 예시다. 실제 사용 가능 모델·가격은 따로 확인해야 한다. 현재 프로필에는 Pydantic AI의 OpenAI 제공자 의존성을 포함했다. 다른 제공자는 공식 어댑터와 의존성을 추가하고 검증한다. 외부 실모델 호출은 미검증이며 TestModel 통과는 LLM 품질 증거가 아니다.

요청당 모델 호출 최대 2회, 모델 설정 timeout 15초·전체 대기 30초, 출력 토큰 한도가 있다. 일일 호출 예산은 UTC 날짜 기준으로 작업공간별 2회를 먼저 예약하며 실패해도 돌려주지 않는다. 반복 실패에 의한 호출 증가를 제한하는 장치이며 달러 비용 하드 캡은 아니다. 이미 전송된 요청 비용은 토큰 한도 오류로 되돌려지지 않는다.

오류나 잘못된 근거 ID가 나오면 rules_fallback을 표시한다. 외부 제공자의 실제 사용량을 알 수 없으므로 이를 비용 0으로 해석하지 않는다.

## 검증 기록

`scripts/verify.py`는 테스트·4개 예제·합성 분류 기준선을 실행하고 `evidence/runtime/`에 결과와 소스 해시를 저장한다. verification.json의 코드 해시와 현재 파일이 다르면 다시 검증한다. baseline-evaluation.json은 분류만 측정하며 fixture의 기대 행동 전체를 점수화하지 않는다.

## 소스와 데이터 복구

검증하며 복구하는 명령: `python scripts/restore_checkpoint.py backups/선택한파일.zip work/restored-copy`. 대상 폴더가 이미 있으면 거부하고, 파일 해시가 다르거나 경로 이탈이 있으면 파일을 쓰기 전에 중단한다.

`python scripts/checkpoint.py before-change`가 만드는 ZIP에는 CHECKPOINT_MANIFEST.json과 파일별 SHA-256이 있다. 기존 작업 위에 덮어쓰지 말고 새 빈 폴더에 풀어 setup → doctor → verify 순서로 확인한다. `.env` 외의 이름으로 저장한 비밀값은 자동 검출하지 않는다. work/의 프로젝트는 각각 자기 폴더에서 백업한다.

`scripts/backup_data.py`는 SQLite online backup API로 WAL 변경도 일관되게 저장하고 integrity_check를 실행한다. 파일은 backups/data-*.sqlite3에 생긴다. 복구 시 서버를 종료한 뒤 새 프로젝트의 빈 runtime-data 폴더에 workbench.sqlite3로 복사한다. 기존 DB·WAL에 덮어쓰지 않는다. 소스 ZIP과 DB 백업은 서로 다른 준비물이다.

## 외부 실행 어댑터 확장

로컬 기록을 외부 API 호출 한 줄로 바꾸면 중복 방지가 보장되지 않는다. 요청 ID·승인 payload·외부 멱등 키를 영속 저장하고 timeout 뒤 실제 처리 여부 조회, 재시도·취소·부분 실패 재조정을 구현해야 한다. 결제·주문은 제공자의 테스트 환경에서 먼저 검증한다.
