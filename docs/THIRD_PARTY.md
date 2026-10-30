# 재사용한 오픈소스와 버전

설치한 정확한 패키지 버전은 requirements.lock에 고정했다. 의존성 배포물과 wheel에 동봉된 라이선스·NOTICE는 유지한다. 아래는 직접 사용하는 주요 구성요소이며 전이 의존성과 실제 배포 방식의 조건까지 이 표 하나로 판단하지 않는다.

| 구성요소 | 이 키트에서의 역할 | 공식 소스 |
|---|---|---|
| FastAPI | API 라우팅·입력 검증 연결 | https://github.com/fastapi/fastapi |
| Pydantic / Pydantic AI | 데이터 형식·모델 응답 검증·모델 어댑터 | https://github.com/pydantic/pydantic-ai |
| Uvicorn | 로컬 HTTP 서버 | https://github.com/encode/uvicorn |
| SQLite | 영속 상태·고유 제약·트랜잭션·백업 | https://sqlite.org/ |
| MarkItDown | 문서 변환 어댑터 | https://github.com/microsoft/markitdown |
| DuckDB | 고정 SQL 집계 | https://github.com/duckdb/duckdb |
| OR-Tools | 제약 기반 일정 배정 | https://github.com/google/or-tools |

GitHub 후보 목록에 있다는 것이 해당 저장소 전체를 복사·설치했다는 뜻은 아니다. 원문 조사 파일은 evidence/github에, 실행 의존성은 .venv와 requirements.lock에 있다. GitHub 저장소는 공개되어 있다. 자체 작성 코드의 재사용 라이선스는 아직 지정하지 않았다. 저장소 공개가 포함된 제3자 자료의 라이선스를 변경하지는 않는다.

사용한 공식 기술 자료: [FastAPI 테스트](https://fastapi.tiangolo.com/tutorial/testing/), [Pydantic AI 테스트](https://pydantic.dev/docs/ai/guides/testing/), [OR-Tools CP-SAT](https://developers.google.com/optimization/cp/cp_solver). 문서와 설치된 버전 사이의 차이는 실제 테스트와 소스 시그니처로 확인했다.
