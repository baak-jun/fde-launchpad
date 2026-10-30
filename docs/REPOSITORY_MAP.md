# 상황별 외부 저장소 지도

기반을 하나 선택하고 필요한 기능만 더합니다. 모두 설치하거나 포크할 필요는 없습니다. 공식 원본은 아래 링크에서 관리되고, 내 정리 저장소 이름은 `fde-launchpad`입니다.

## 앱 기반과 제작 도구

| 선택할 상황 | 공식 저장소 | 키트에서 시작 |
|---|---|---|
| Python API·React 서비스 | [fastapi/full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template) | `python kit.py prepare web my-web --fetch` |
| 자유 디자인의 관리 화면 | [refinedev/refine](https://github.com/refinedev/refine) | `python kit.py prepare admin my-admin --fetch` |
| 데이터·권한·폼·보고서 중심 | [frappe/frappe](https://github.com/frappe/frappe) | `python kit.py prepare business my-business --fetch` |
| RAG·AI 워크플로 | [langgenius/dify](https://github.com/langgenius/dify) | `python kit.py prepare ai my-ai --fetch` |
| 기존 API·DB의 사내 도구 | [appsmithorg/appsmith](https://github.com/appsmithorg/appsmith) | `python kit.py prepare internal my-internal --fetch` |
| 로컬 AI 앱 제작 | [dyad-sh/dyad](https://github.com/dyad-sh/dyad) | `python kit.py prepare dyad my-builder --fetch` |
| 브라우저 AI 앱 제작 | [stackblitz-labs/bolt.diy](https://github.com/stackblitz-labs/bolt.diy) | `python kit.py prepare bolt my-builder --fetch` |
| 개발 환경 재현 | [devcontainers/templates](https://github.com/devcontainers/templates) | 현재 `.devcontainer` 설정 또는 외부 앱의 전용 설정 사용 |

조사 기준: 2026-10-30 공식 README·라이선스. 실제 선택 기준과 통합 순서는 [시작 가이드](START_BY_PROBLEM.md)를 따릅니다. 외부 프로젝트의 README는 계속 변경되므로 가져온 커밋과 설치 결과를 프로젝트에 남깁니다.

## 필요한 기능만 추가

아래 항목은 기존 28개 조사 목록의 선택 예시입니다. 라이선스와 조건은 [전체 목록](REPOSITORIES.md)에서 확인하세요. 목록에 있는 것과 통합·검증 완료는 다릅니다.

| 필요 기능 | 우선 후보 | 연결 지점 |
|---|---|---|
| 문서 변환 | [MarkItDown](https://github.com/microsoft/markitdown), [Docling](https://github.com/docling-project/docling) | 입력 문서를 텍스트·구조로 변환 |
| 검색과 RAG | [LlamaIndex](https://github.com/run-llama/llama_index), [pgvector](https://github.com/pgvector/pgvector) | 검색·근거·권한 필터 |
| Python 구조화 AI | [Pydantic AI](https://github.com/pydantic/pydantic-ai) | 기존 어댑터를 확장 |
| TypeScript AI UI | [Vercel AI SDK](https://github.com/vercel/ai) | React 앱의 스트리밍·도구 호출 |
| 자동화 연결 | [Activepieces](https://github.com/activepieces/activepieces), [n8n](https://github.com/n8n-io/n8n) | 승인된 업무의 후속 처리; 상용·소스 공개 조건 구분 |
| 표 분석·배정 | [DuckDB](https://github.com/duckdb/duckdb), [OR-Tools](https://github.com/google/or-tools) | 현재 합성 예제를 실제 데이터로 확장 |
| AI 평가·관측 | [promptfoo](https://github.com/promptfoo/promptfoo), [Langfuse](https://github.com/langfuse/langfuse) | 평가 데이터·실행 비용·실패 추적 |
| 모바일 앱 | [Expo](https://github.com/expo/expo), [Flutter](https://github.com/flutter/flutter) | 별도 네이티브 앱 프로젝트; 기기 검증 필요 |
| 음성 | [LiveKit Agents](https://github.com/livekit/agents), [Whisper](https://github.com/openai/whisper) | 음성 입출력 경로 |
| 커머스·ERP | [Medusa](https://github.com/medusajs/medusa), [ERPNext](https://github.com/frappe/erpnext) | 도메인 원장과 업무 규칙 |

## 라이선스 경계

- FastAPI Template·Frappe Framework·Dev Container Templates: 공식 README의 MIT 안내 기준.
- Appsmith: 공개 저장소 루트 Apache-2.0. 유료 제품 기능까지 포함된 것으로 보지 않습니다.
- Dyad: 일반 코드 Apache-2.0, `src/pro`는 FSL. [원본 안내](https://github.com/dyad-sh/dyad#license).
- bolt.diy: MIT, WebContainers 상용 조건 별도. [원본 안내](https://github.com/stackblitz-labs/bolt.diy#licensing).
- Dify: 수정 Apache-2.0 조건으로 멀티테넌트 서비스·프런트엔드 로고 제한이 있습니다. [원본 라이선스](https://github.com/langgenius/dify/blob/main/LICENSE).
- Refine: 여기서 비교한 대상은 공개 Core입니다. 유료 AI 제작 서비스와 구분합니다.

내 저장소에는 이 선택 지도와 연결 명령을 보관합니다. 내려받은 외부 프로젝트는 `work/`에 두므로 원본 키트 Git에 포함되지 않습니다. 실제로 개발할 앱을 골랐을 때 해당 프로젝트만 별도 저장소로 옮기고 원본 라이선스를 유지하세요.
