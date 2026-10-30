# 테마별 DESIGN.md 라이브러리

**v2 업데이트:** [완성 화면의 구조를 비교하는 새 갤러리](index.html)에 한국 8종과 해외 4종을 추가했다. 기존 12종과 합쳐 총 24종이다. [새 자료의 출처·원본과 응용 시안 구분](SHOWCASE.md)을 먼저 확인한다. 아래의 12종 목록은 [기존 토큰 갤러리](token-gallery.html)에 보존했다.

**[스크린샷 갤러리 열기](index.html)**. 파일을 브라우저에서 열면 별도 설치 없이 검색·분류·밝음/어두움 비교를 사용할 수 있다.

인터넷의 공개 디자인 분석을 12개 방향으로 골랐다. 브랜드 공식 문서가 아니라 커뮤니티가 분석한 참고 자료다. MD와 스크린샷이 대응하도록 ropean의 같은 저장소 스냅샷을 보관했다. 최신 VoltAgent 본문은 개편되어 미리보기와 차이가 있을 수 있으므로 서로 섞지 않았다.

## 어떤 것을 고를까

| 테마 | 권장 용도 | 안내 |
|---|---|---|
| Claude · 따뜻한 에디토리얼 | 상담 기록·리서치·읽기 | [보기](claude/APPLY.md) |
| Notion · 담백한 워크스페이스 | 문서·위키·편집 | [보기](notion/APPLY.md) |
| Linear · 정밀한 다크 콘솔 | 이슈·작업 큐·운영 | [보기](linear.app/APPLY.md) |
| Vercel · 흑백 테크니컬 | API·로그·배포 | [보기](vercel/APPLY.md) |
| IBM · 엔터프라이즈 그리드 | 승인·관리·정책 | [보기](ibm/APPLY.md) |
| Stripe · 정돈된 금융 서비스 | 정산·사용량·결제 | [보기](stripe/APPLY.md) |
| Airbnb · 친근한 탐색과 예약 | 예약·검색·지역 서비스 | [보기](airbnb/APPLY.md) |
| Miro · 밝은 협업 캔버스 | 워크숍·교육·협업 | [보기](miro/APPLY.md) |
| Spotify · 몰입형 미디어 | 음성·영상·라이브러리 | [보기](spotify/APPLY.md) |
| BMW · 각진 프리미엄 | 하드웨어·제품 소개 | [보기](bmw/APPLY.md) |
| PostHog · 개성 있는 개발자 편집물 | 커뮤니티·실험 노트 | [보기](posthog/APPLY.md) |
| Mintlify · 선명한 문서 포털 | 문서·온보딩·도움말 | [보기](mintlify/APPLY.md) |

## 바로 가져다 쓰기

1. 갤러리에서 한 테마를 고르고 한국어 안내를 읽는다.
2. 프로젝트에 `design-library/`를 복사한다. 키트의 `python kit.py start 새이름`에도 이 폴더가 포함된다.
3. 선택 테마의 **적용 프롬프트 복사**를 눌러 AI에게 전달한다. 자동 복사가 안 되면 PROMPT.txt를 사용한다.
4. 실제 사용자 흐름·유지할 기능·대상 화면을 지시문에 추가한다. 전체 테마를 한꺼번에 읽힐 필요는 없다.

예: `design-library/COMMON_RULES.md`, `design-library/ibm/APPLY.md`, `design-library/ibm/DESIGN.md`를 읽고 승인 목록 화면에 적용해줘.

각 테마 폴더에는 원본 DESIGN.md, 한국어 APPLY.md, 적용 PROMPT.txt, 밝음/어두움 스크린샷 2장과 전체 HTML 예시가 있다. 스크린샷은 토큰·컴포넌트 예시의 저장소 제공 캡처이며 실제 브랜드 제품 화면은 아니다. 전체 HTML은 Google Fonts를 요청할 수 있고 오프라인에서는 대체 폰트를 사용한다. MD와 캡처 자체는 오프라인에서 열 수 있다.

## 출처와 보관

- [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md): 디자인 분석 모음. 최신 원본도 조사했으나 미리보기와 버전 차이를 확인했다.
- [ropean/awesome-design-md-preview](https://github.com/ropean/awesome-design-md-preview): 이번에 보관한 MD·HTML·스크린샷의 직접 출처.
- 확인일 2026-10-26. [manifest.json](manifest.json)에 파일별 SHA-256·원본 URL·다운로드 ZIP 해시를 저장했다.
- 두 저장소의 MIT 라이선스를 보관했다. 브랜드의 로고·사진·독점 폰트는 이 문서의 라이선스로 사용 허가되는 것이 아니다.

현재 업무 실험실 UI에는 특정 테마를 적용하지 않았다. 이 폴더는 선택·재사용용 라이브러리다. 이전에 만든 FDE 오프라인 번들에는 이 신규 라이브러리가 없으므로 새 디자인 번들 또는 최신 소스 백업을 함께 사용한다.
