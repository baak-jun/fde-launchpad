# 문제별 오픈소스 후보 28개

이 목록의 실행 상태는 초기 조사 시점의 기록이다. 이후 Pydantic AI·MarkItDown·DuckDB·OR-Tools의 일부 API를 실제 예제로 검증했다. 현재 설치·실행 범위는 [검증 기록](VALIDATION.md)을 기준으로 읽는다. 라이브러리 예제 검증과 해당 레포 전체 제품의 검증은 다르다.

조사 기준일: 2026-10-26 KST. 공식 README·GitHub 메타데이터·루트 LICENSE 기반. 모든 후보의 앱 실행은 미검증이다. 기본은 우선 학습 후보라는 뜻이며 모두 설치하라는 뜻은 아니다.

## 빠른 비교

| 문제 | 후보 | 선택 시점 | 구분 | 라이선스 요약 |
|---|---|---|---|---|
| 웹 서비스 기반 | [fastapi/full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template) | Python API·React·DB가 필요한 업무 제품 | 기본 | MIT |
| AI 인터페이스 | [vercel/ai](https://github.com/vercel/ai) | TypeScript 스트리밍·도구 호출·구조화 출력 | 기본 | Apache-2.0 |
| 구조화 AI | [pydantic/pydantic-ai](https://github.com/pydantic/pydantic-ai) | Python에서 타입 검증과 도구 호출이 필요한 작업 | 기본 | MIT |
| 상태 기반 에이전트 | [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) | 중단·재개·사람 확인이 필요한 다단계 업무 | 조건부 | MIT |
| 문서 변환 | [microsoft/markitdown](https://github.com/microsoft/markitdown) | 여러 사무 문서를 텍스트로 통일 | 기본 | MIT |
| 문서 구조 분석 | [docling-project/docling](https://github.com/docling-project/docling) | PDF 표·레이아웃·OCR가 중요한 문제 | 조건부 | MIT |
| 문서 검색 구성 | [run-llama/llama_index](https://github.com/run-llama/llama_index) | 수집·색인·검색 파이프라인이 필요한 RAG | 조건부 | MIT |
| 벡터 검색 | [pgvector/pgvector](https://github.com/pgvector/pgvector) | PostgreSQL 데이터와 의미 검색을 함께 운영 | 기본 | PostgreSQL License |
| 표 데이터 분석 | [duckdb/duckdb](https://github.com/duckdb/duckdb) | CSV·Parquet를 SQL로 분석하는 문제 | 기본 | MIT |
| 빠른 데이터 UI | [streamlit/streamlit](https://github.com/streamlit/streamlit) | 분석·AI 결과를 즉시 조작하는 데모 | 기본 | Apache-2.0 |
| 업무 앱 연결 | [activepieces/activepieces](https://github.com/activepieces/activepieces) | 이메일·시트·CRM 연계 자동화 | 조건부 | MIT core; EE separate |
| 업무 앱 연결 대안 | [n8n-io/n8n](https://github.com/n8n-io/n8n) | 기존 n8n 경험이나 특정 커넥터가 있을 때 | 제약검토 | Sustainable Use License; EE separate |
| 시각적 AI 워크플로 | [langgenius/dify](https://github.com/langgenius/dify) | 코드보다 시각적 RAG·에이전트 시연이 우선 | 제약검토 | Dify license (Apache-2.0 + additional conditions) |
| AI 평가 | [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) | 프롬프트·모델 변경 전후 비교 | 기본 | MIT |
| AI 관측 | [langfuse/langfuse](https://github.com/langfuse/langfuse) | 실행별 비용·지연·실패 원인 추적 | 조건부 | MIT core; EE separate |
| 계획 최적화 | [google/or-tools](https://github.com/google/or-tools) | 일정·배차·배정·자원 제약 최적화 | 조건부 | Apache-2.0 |
| 추천 | [benfred/implicit](https://github.com/benfred/implicit) | 사용자·아이템 상호작용 기반 추천 | 조건부 | MIT |
| 시각 이상 탐지 | [open-edge-platform/anomalib](https://github.com/open-edge-platform/anomalib) | 제조 이미지·검사 결함 탐지 | 조건부 | Apache-2.0 |
| 음성 전사 | [openai/whisper](https://github.com/openai/whisper) | 녹음에서 텍스트를 추출 | 조건부 | MIT |
| 실시간 음성 | [livekit/agents](https://github.com/livekit/agents) | 음성 대화와 실시간 에이전트 | 조건부 | Apache-2.0 |
| 커머스 | [medusajs/medusa](https://github.com/medusajs/medusa) | 카탈로그·장바구니·주문이 중심인 제품 | 도메인베이스 | MIT core; Enterprise separate |
| 업무 시스템 | [frappe/erpnext](https://github.com/frappe/erpnext) | 재고·구매·회계 등 ERP 업무 | 도메인베이스 | GPL-3.0 |
| 예약 | [calcom/cal.diy](https://github.com/calcom/cal.diy) | 가용 시간·일정 예약이 핵심 | 도메인베이스 | MIT |
| 관리자 업무 UI | [marmelab/react-admin](https://github.com/marmelab/react-admin) | 리소스 CRUD·필터·관리 화면 | 기본 | MIT |
| 다중 플랫폼 UI | [flutter/flutter](https://github.com/flutter/flutter) | 모바일·데스크톱 네이티브 UI가 핵심 | 조건부 | BSD-3-Clause |
| React 모바일 UI | [expo/expo](https://github.com/expo/expo) | React 경험으로 모바일 기능 시연 | 조건부 | MIT |
| 로컬 모델 실행 | [ollama/ollama](https://github.com/ollama/ollama) | 외부 모델 API 없이 로컬 추론 | 조건부 | MIT |
| 장기 업무 실행 | [temporalio/temporal](https://github.com/temporalio/temporal) | 재시도·복구가 필요한 장기 프로세스 | 조건부 | MIT |

## 선택 시 확인할 점

라이선스 표는 루트 파일의 분류다. 실제 가져갈 커밋·하위 패키지·모델·데이터의 조건과 고지 파일을 함께 확인한다. 최종 제품 전체의 이용 가능성을 이 표만으로 판단하지 않는다. last push는 유지보수의 단서이며 품질·보안 보증이나 최신 릴리스 날짜가 아니다.

### fastapi/full-stack-fastapi-template

Docker와 DB 운영 필요; AI·도메인 규칙은 별도

- 최근 push UTC: 2026-10-26T03:21:46Z; archived: False
- [공식 README](https://raw.githubusercontent.com/fastapi/full-stack-fastapi-template/master/README.md) · [루트 라이선스](https://raw.githubusercontent.com/fastapi/full-stack-fastapi-template/master/LICENSE)
- 로컬 증거: `evidence/github/fastapi__full-stack-fastapi-template/`

### vercel/ai

SDK이며 완성 앱이 아님; 모델 비용 별도

- 최근 push UTC: 2026-10-26T00:34:24Z; archived: False
- [공식 README](https://raw.githubusercontent.com/vercel/ai/main/README.md) · [루트 라이선스](https://raw.githubusercontent.com/vercel/ai/main/LICENSE)
- 로컬 증거: `evidence/github/vercel__ai/`

### pydantic/pydantic-ai

검증된 JSON도 사실 정확성을 보장하지 않음

- 최근 push UTC: 2026-10-26T03:50:14Z; archived: False
- [공식 README](https://raw.githubusercontent.com/pydantic/pydantic-ai/main/README.md) · [루트 라이선스](https://raw.githubusercontent.com/pydantic/pydantic-ai/main/LICENSE)
- 로컬 증거: `evidence/github/pydantic__pydantic-ai/`

### langchain-ai/langgraph

단일 모델 호출에는 과함; 영속 저장소 설정 필요

- 최근 push UTC: 2026-10-26T04:36:24Z; archived: False
- [공식 README](https://raw.githubusercontent.com/langchain-ai/langgraph/main/README.md) · [루트 라이선스](https://raw.githubusercontent.com/langchain-ai/langgraph/main/LICENSE)
- 로컬 증거: `evidence/github/langchain-ai__langgraph/`

### microsoft/markitdown

스캔·복잡한 표 품질은 입력별 검증

- 최근 push UTC: 2026-10-23T17:04:06Z; archived: False
- [공식 README](https://raw.githubusercontent.com/microsoft/markitdown/main/README.md) · [루트 라이선스](https://raw.githubusercontent.com/microsoft/markitdown/main/LICENSE)
- 로컬 증거: `evidence/github/microsoft__markitdown/`

### docling-project/docling

모델 다운로드와 CPU·메모리·처리시간 확인

- 최근 push UTC: 2026-10-25T10:47:00Z; archived: False
- [공식 README](https://raw.githubusercontent.com/docling-project/docling/main/README.md) · [루트 라이선스](https://raw.githubusercontent.com/docling-project/docling/main/LICENSE)
- 로컬 증거: `evidence/github/docling-project__docling/`

### run-llama/llama_index

처음부터 모든 커넥터 설치하지 않기

- 최근 push UTC: 2026-10-23T13:51:39Z; archived: False
- [공식 README](https://raw.githubusercontent.com/run-llama/llama_index/main/README.md) · [루트 라이선스](https://raw.githubusercontent.com/run-llama/llama_index/main/LICENSE)
- 로컬 증거: `evidence/github/run-llama__llama_index/`

### pgvector/pgvector

별도 DB 기능; 임베딩·권한·평가는 직접 구성

- 최근 push UTC: 2026-10-25T20:20:18Z; archived: False
- [공식 README](https://raw.githubusercontent.com/pgvector/pgvector/master/README.md) · [루트 라이선스](https://raw.githubusercontent.com/pgvector/pgvector/master/LICENSE)
- 로컬 증거: `evidence/github/pgvector__pgvector/`

### duckdb/duckdb

사용자 임의 SQL 실행은 제한; 동시 쓰기 제품 DB 대용 아님

- 최근 push UTC: 2026-10-23T19:39:03Z; archived: False
- [공식 README](https://raw.githubusercontent.com/duckdb/duckdb/main/README.md) · [루트 라이선스](https://raw.githubusercontent.com/duckdb/duckdb/main/LICENSE)
- 로컬 증거: `evidence/github/duckdb__duckdb/`

### streamlit/streamlit

복잡한 모바일 UX와 다중 사용자 업무 흐름에는 별도 설계

- 최근 push UTC: 2026-10-26T04:44:24Z; archived: False
- [공식 README](https://raw.githubusercontent.com/streamlit/streamlit/develop/README.md) · [루트 라이선스](https://raw.githubusercontent.com/streamlit/streamlit/develop/LICENSE)
- 로컬 증거: `evidence/github/streamlit__streamlit/`

### activepieces/activepieces

커뮤니티·기업 기능 라이선스 분리; 연결별 권한 확인

- 최근 push UTC: 2026-10-26T03:52:50Z; archived: False
- [공식 README](https://raw.githubusercontent.com/activepieces/activepieces/main/README.md) · [루트 라이선스](https://raw.githubusercontent.com/activepieces/activepieces/main/LICENSE)
- 로컬 증거: `evidence/github/activepieces__activepieces/`

### n8n-io/n8n

source-available; 범용 재판매·호스팅 키트 기본값에서 제외

- 최근 push UTC: 2026-10-26T00:47:05Z; archived: False
- [공식 README](https://raw.githubusercontent.com/n8n-io/n8n/master/README.md) · [루트 라이선스](https://raw.githubusercontent.com/n8n-io/n8n/master/LICENSE.md)
- 로컬 증거: `evidence/github/n8n-io__n8n/`

### langgenius/dify

추가 조건 라이선스; 다중 테넌트·브랜딩 조건 확인

- 최근 push UTC: 2026-10-26T04:44:04Z; archived: False
- [공식 README](https://raw.githubusercontent.com/langgenius/dify/main/README.md) · [루트 라이선스](https://raw.githubusercontent.com/langgenius/dify/main/LICENSE)
- 로컬 증거: `evidence/github/langgenius__dify/`

### promptfoo/promptfoo

평가 모델 호출 비용 별도; 기대값과 실패 기준 직접 작성

- 최근 push UTC: 2026-10-26T04:44:12Z; archived: False
- [공식 README](https://raw.githubusercontent.com/promptfoo/promptfoo/main/README.md) · [루트 라이선스](https://raw.githubusercontent.com/promptfoo/promptfoo/main/LICENSE)
- 로컬 증거: `evidence/github/promptfoo__promptfoo/`

### langfuse/langfuse

EE 기능 별도 조건; 자체 호스팅 서비스 수 확인

- 최근 push UTC: 2026-10-26T04:38:09Z; archived: False
- [공식 README](https://raw.githubusercontent.com/langfuse/langfuse/main/README.md) · [루트 라이선스](https://raw.githubusercontent.com/langfuse/langfuse/main/LICENSE)
- 로컬 증거: `evidence/github/langfuse__langfuse/`

### google/or-tools

LLM은 제약 추출만; 해법과 불가능 조건은 solver로 검증

- 최근 push UTC: 2026-10-23T21:14:06Z; archived: False
- [공식 README](https://raw.githubusercontent.com/google/or-tools/stable/README.md) · [루트 라이선스](https://raw.githubusercontent.com/google/or-tools/stable/LICENSE)
- 로컬 증거: `evidence/github/google__or-tools/`

### benfred/implicit

cold start와 학습 데이터 부족 시 규칙 기반 대안

- 최근 push UTC: 2026-05-08T19:01:37Z; archived: False
- [공식 README](https://raw.githubusercontent.com/benfred/implicit/main/README.md) · [루트 라이선스](https://raw.githubusercontent.com/benfred/implicit/main/LICENSE)
- 로컬 증거: `evidence/github/benfred__implicit/`

### open-edge-platform/anomalib

도메인 이미지와 모델·장치별 추론 검증 필요

- 최근 push UTC: 2026-10-24T02:24:22Z; archived: False
- [공식 README](https://raw.githubusercontent.com/open-edge-platform/anomalib/main/README.md) · [루트 라이선스](https://raw.githubusercontent.com/open-edge-platform/anomalib/main/LICENSE)
- 로컬 증거: `evidence/github/open-edge-platform__anomalib/`

### openai/whisper

모델 다운로드·FFmpeg·언어별 품질·실시간 지연 확인

- 최근 push UTC: 2026-08-31T17:19:19Z; archived: False
- [공식 README](https://raw.githubusercontent.com/openai/whisper/main/README.md) · [루트 라이선스](https://raw.githubusercontent.com/openai/whisper/main/LICENSE)
- 로컬 증거: `evidence/github/openai__whisper/`

### livekit/agents

전송 서버·STT·LLM·TTS 각각의 비용과 연결 필요

- 최근 push UTC: 2026-10-26T04:22:26Z; archived: False
- [공식 README](https://raw.githubusercontent.com/livekit/agents/main/README.md) · [루트 라이선스](https://raw.githubusercontent.com/livekit/agents/main/LICENSE)
- 로컬 증거: `evidence/github/livekit__agents/`

### medusajs/medusa

MIT core와 Enterprise 코드 분리; 결제·배송·세금은 별도 통합

- 최근 push UTC: 2026-10-25T21:46:11Z; archived: False
- [공식 README](https://raw.githubusercontent.com/medusajs/medusa/develop/README.md) · [루트 라이선스](https://raw.githubusercontent.com/medusajs/medusa/develop/LICENSE)
- 로컬 증거: `evidence/github/medusajs__medusa/`

### frappe/erpnext

GPL 계열; 무거운 배포와 도메인 학습 비용

- 최근 push UTC: 2026-10-26T04:24:26Z; archived: False
- [공식 README](https://raw.githubusercontent.com/frappe/erpnext/develop/README.md) · [루트 라이선스](https://raw.githubusercontent.com/frappe/erpnext/develop/license.txt)
- 로컬 증거: `evidence/github/frappe__erpnext/`

### calcom/cal.diy

MIT Cal.diy; 기존 cal.com 링크가 이 저장소로 이동. 팀·조직·SSO 등 EE 기능 제거; 상용 Cal.com과 구분

- 최근 push UTC: 2026-10-19T18:46:00Z; archived: False
- [공식 README](https://raw.githubusercontent.com/calcom/cal.diy/main/README.md) · [루트 라이선스](https://raw.githubusercontent.com/calcom/cal.diy/main/LICENSE)
- 로컬 증거: `evidence/github/calcom__cal.com/`

### marmelab/react-admin

프런트엔드 프레임워크; 데이터 API·기업 기능 별도

- 최근 push UTC: 2026-10-25T14:35:23Z; archived: False
- [공식 README](https://raw.githubusercontent.com/marmelab/react-admin/master/README.md) · [루트 라이선스](https://raw.githubusercontent.com/marmelab/react-admin/master/LICENSE.md)
- 로컬 증거: `evidence/github/marmelab__react-admin/`

### flutter/flutter

장치 권한·플러그인별 플랫폼 지원은 따로 검증

- 최근 push UTC: 2026-10-25T04:29:27Z; archived: False
- [공식 README](https://raw.githubusercontent.com/flutter/flutter/master/README.md) · [루트 라이선스](https://raw.githubusercontent.com/flutter/flutter/master/LICENSE)
- 로컬 증거: `evidence/github/flutter__flutter/`

### expo/expo

네이티브 모듈·개발 빌드·실기기 사전 준비

- 최근 push UTC: 2026-10-26T00:57:04Z; archived: False
- [공식 README](https://raw.githubusercontent.com/expo/expo/main/README.md) · [루트 라이선스](https://raw.githubusercontent.com/expo/expo/main/LICENSE)
- 로컬 증거: `evidence/github/expo__expo/`

### ollama/ollama

런타임과 모델의 라이선스 별개; 메모리·속도 확인

- 최근 push UTC: 2026-10-26T04:25:58Z; archived: False
- [공식 README](https://raw.githubusercontent.com/ollama/ollama/main/README.md) · [루트 라이선스](https://raw.githubusercontent.com/ollama/ollama/main/LICENSE)
- 로컬 증거: `evidence/github/ollama__ollama/`

### temporalio/temporal

짧은 해커톤 기본 구성에서 제외; 서버 운영 비용

- 최근 push UTC: 2026-10-26T02:44:24Z; archived: False
- [공식 README](https://raw.githubusercontent.com/temporalio/temporal/main/README.md) · [루트 라이선스](https://raw.githubusercontent.com/temporalio/temporal/main/LICENSE)
- 로컬 증거: `evidence/github/temporalio__temporal/`
