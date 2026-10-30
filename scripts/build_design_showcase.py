"""Import cited design studies and build a screen-first local lookbook.
Run with the kit venv; requires the two research ZIPs in .cache/design-research.
"""
from pathlib import Path
from zipfile import ZipFile
from bs4 import BeautifulSoup
import html, json, hashlib, re

ROOT=Path(__file__).resolve().parents[1]
LIB=ROOT/'design-library'
KR=[
 ('toss','토스','모바일 금융','큰 숫자와 단계별 송금','개인 금융·신청 절차·결제 확인','Send-Money flow'),
 ('zigbang','직방','지도·탐색','지도와 필터, 매물 상세','공간 검색·현장 방문·지역 서비스','웹 아파트 지도'),
 ('greeting','그리팅','업무 콘솔','사이드바와 촘촘한 지원자 표','승인 큐·CRM·채용 관리','Greeting ATS'),
 ('ridi','리디','콘텐츠 서가','표지와 가로 탐색, 콘텐츠의 밀도','웹툰·문서 라이브러리·교육 콘텐츠','04 화면'),
 ('kyobobook','교보문고','읽기·커머스','책 정보와 여백이 만드는 위계','도서·지식 큐레이션·리뷰','책을 읽듯'),
 ('baemin','배달의민족','브랜드·커머스','민트색 면과 굵은 한글의 리듬','지역 커머스·음식·친근한 브랜드','세상 모든 것이'),
 ('samsung-one-ui','삼성 One UI','모바일 설정','보기 영역과 조작 영역의 분리','설정·기기 연동·모바일 유틸리티','뷰잉 / 인터랙션'),
 ('nol','NOL','여행·탐색','검색창과 다채로운 목적지 선택','여행·예약·이벤트 탐색','웹 홈'),
]
GLOBAL=[
 ('oura','Oura','웰니스 에디토리얼','크림색 종이와 세리프, 비대칭 구성','건강 기록·리서치·라이프스타일'),
 ('wired','WIRED','매거진','신문형 다단 편집과 강한 제목 대비','뉴스·리포트·전문 콘텐츠'),
 ('dell-1996','Dell 1996','레트로 카탈로그','검정 프레임과 평면 색띠','제품 카탈로그·개성 있는 포트폴리오'),
 ('nintendo-2001','Nintendo 2001','Y2K 게임 포털','베벨 패널과 콘솔 같은 내비게이션','게임·커뮤니티·팬 프로젝트'),
]

def write(path,text):
 path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding='utf-8')

def global_screen(slug):
 base='''*{box-sizing:border-box}body{margin:0;font-family:Arial,"Malgun Gothic",sans-serif;color:#202020}a{color:inherit}h1,h2,p{margin:0}p{line-height:1.7}.stamp{font:11px/1.5 monospace;letter-spacing:1px;padding:12px 24px;background:#222;color:#fff}.app{min-height:740px}header{display:flex;justify-content:space-between;align-items:center;padding:24px 36px;border-bottom:1px solid #7775}nav{font-size:13px;word-spacing:22px}.label{font:12px monospace;letter-spacing:2px}.cta{display:inline-block;margin-top:24px;padding:14px 22px;background:#222;color:white;border-radius:2px;font-size:14px}.foot{font-size:12px;padding:16px 30px;border-top:1px solid #8885}@media(max-width:700px){.split,.news,.catalog,.portal{display:block!important}.panel{margin:12px!important}h1{font-size:42px!important}nav{display:none}.app{min-height:0}}'''
 if slug=='oura':
  css='''body{background:#f7f1e8;color:#39221e}header strong{font:30px Georgia}.split{display:grid;grid-template-columns:1fr 1fr;gap:60px;padding:52px 60px}.split h1{font:76px/1.02 Georgia,serif;margin:24px 0}.split p{max-width:380px}.cta{border-radius:40px;background:#2a72de}.art{background:#ced4b8;border-radius:220px 220px 0 0;position:relative;min-height:430px;overflow:hidden}.ring{width:220px;height:220px;border:38px solid #af751b;border-radius:50%;position:absolute;top:82px;left:50%;transform:translateX(-50%) rotate(-25deg);box-shadow:inset 6px 6px 0 #684d07,12px 18px 0 #849671}.art small{position:absolute;bottom:30px;left:30px}.metrics{display:flex;justify-content:space-around;border-top:1px solid #6b443d55;padding:24px}.metrics b{font:34px Georgia}'''
  body='''<header><strong>Daylight journal</strong><nav>기록 인사이트 나의 리듬</nav></header><div class="split"><div><div class="label">A QUIETER WAY TO BEGIN</div><h1>Make room<br>for your rhythm.</h1><p>바쁜 하루를 채우기 전에, 내 몸의 흐름부터 읽어보세요. 작은 기록으로 시작하는 오늘의 리듬.</p><span class="cta">오늘의 기록 열기 →</span></div><div class="art"><div class="ring"></div><small>CSS 도형으로 만든 제품 연구 · 사진 아님</small></div></div><div class="metrics"><div><b>07:30</b><p>기상 기록</p></div><div><b>24 min</b><p>아침 산책</p></div><div><b>Calm</b><p>오늘의 메모</p></div></div>'''
 elif slug=='wired':
  css='''body{background:#fff;color:#000}header{border-bottom:8px solid #000}header strong{font:900 40px "Arial Black",sans-serif;letter-spacing:-3px}.news{display:grid;grid-template-columns:1.5fr .8fr;gap:32px;margin:30px 36px}.lead{border-right:1px solid #000;padding-right:30px}.lead h1{font:58px/1.04 Georgia,serif;margin:18px 0}.lead p{font:18px/1.7 Georgia,"Batang",serif}.diagram{height:210px;background:#e7ff58;position:relative;overflow:hidden;margin:24px 0}.diagram span{position:absolute;width:170px;height:170px;border:2px solid #111;border-radius:50%;top:20px}.diagram span:nth-child(1){left:15%}.diagram span:nth-child(2){left:35%}.diagram span:nth-child(3){left:55%}aside article{padding:20px 0;border-bottom:1px solid #000}aside h2{font:27px/1.25 Georgia;margin:12px 0}.label{font-weight:bold}'''
  body='''<header><strong>FIELD / NOTES</strong><nav>TECH SCIENCE CULTURE IDEAS</nav></header><div class="news"><article class="lead"><div class="label">THE BIG READ / 08 MIN</div><h1>Who decides<br>what your agent<br>does next?</h1><div class="diagram"><span></span><span></span><span></span></div><p>자동화의 속도보다 중요한 질문. 실행 권한과 책임을 어디에 둘 것인가.</p></article><aside><div class="label">LATEST THINKING</div><article><small>01 — SYSTEMS</small><h2>AI가 멈춰야 할 순간을 설계하는 사람들</h2><p>기술 리포트 · 예시 콘텐츠</p></article><article><small>02 — CULTURE</small><h2>더 적은 화면, 더 분명한 결정</h2><p>디자인 에세이 · 예시 콘텐츠</p></article><article><small>03 — FIELDWORK</small><h2>현장에서 배운 여섯 가지 실패</h2></article></aside></div>'''
 elif slug=='dell-1996':
  css='''body{background:#000;padding:22px}.app{background:#fff;border:8px solid #000;max-width:1100px;margin:auto}header{background:#000;color:white;padding:20px}header strong{font:900 34px "Arial Black"}.catalog{display:grid;grid-template-columns:210px 1fr;gap:20px;padding:22px}.catalog aside{background:#8c9ae0;padding:22px;border:2px solid black}.catalog aside p{border-bottom:1px solid #000;padding:14px 0;font-family:"Times New Roman",serif}.ribbon{display:grid;grid-template-columns:1fr 150px;min-height:142px;border:2px solid #000;margin-bottom:16px;padding:16px;background:#b3bd95}.ribbon:nth-child(2){background:#d77a7a}.ribbon:nth-child(3){background:#9ab6c8}.ribbon h2{font:900 30px "Arial Black"}.ribbon p{font-family:"Times New Roman",serif}.computer{border:12px solid #ccc;border-bottom-width:25px;background:#242f67;height:95px;box-shadow:5px 5px #333}.sale{background:#fcc20f;color:#000;padding:6px 12px;font-weight:bold;display:inline-block;transform:rotate(-7deg)}'''
  body='''<header><strong>BYTE / SUPPLY</strong><span class="sale">FALL 1996</span></header><div class="catalog"><aside><b>THE CATALOG</b><p>Desktop Systems</p><p>Workstations</p><p>Portable PCs</p><p>Service & Support</p><a href="#">Build your own →</a></aside><main><div class="ribbon"><div><h2>THE WORKHORSE.</h2><p>A dependable desktop for every desk.</p><b>MODEL 01 / SAMPLE</b></div><div class="computer"></div></div><div class="ribbon"><div><h2>POWER TO CREATE.</h2><p>For the next big thing on your screen.</p><b>MODEL 02 / SAMPLE</b></div><div class="computer"></div></div><div class="ribbon"><div><h2>TAKE IT WITH YOU.</h2><p>Your work. Anywhere you go.</p><b>MODEL 03 / SAMPLE</b></div><div class="computer"></div></div></main></div>'''
 else:
  css='''body{background:#3d4f97;padding:24px}.app{max-width:1120px;margin:auto;background:#7a8aba;border:5px ridge #c0d5e6}header{background:#21242e;color:#ecab37;border:4px outset #8ba1d4}header strong{font:bold 32px Arial;font-style:italic}.portal{display:grid;grid-template-columns:180px 1fr 220px;gap:16px;padding:18px}.panel{border:4px ridge #c0d5e6;background:#dedede;margin-bottom:18px}.panel h2{background:#3d4f97;color:white;font-size:16px;padding:9px}.panel p{padding:14px;font-size:13px}.stage{height:315px;background:repeating-linear-gradient(0deg,#206479,#206479 19px,#357d8f 20px);position:relative;border:4px inset #9fbee7;text-align:center;padding-top:50px}.stage h1{font:900 italic 48px/1 Arial;color:#fff;text-shadow:4px 4px #21242e}.orb{height:110px;width:110px;display:inline-block;border-radius:30px;background:#f68d1f;border:8px outset #ecab37;transform:rotate(-12deg);margin-top:22px}.tabs{background:#21242e;color:#ecab37;padding:12px;text-align:center;word-spacing:22px}.newsline{padding:12px;border-bottom:1px solid #60619c;background:#c0d5e6;font-size:13px}'''
  body='''<header><strong>ORBIT / PLAY</strong><nav>GAMES SYSTEMS CLUB SUPPORT</nav></header><div class="tabs">NOW PLAYING / NEW RELEASES / PLAYER CLUB</div><div class="portal"><aside><div class="panel"><h2>SELECT SYSTEM</h2><p>HOME CONSOLE</p><p>HANDHELD</p><p>CLASSICS</p></div><div class="panel"><h2>PLAYER LOGIN</h2><p>WELCOME BACK<br>PLAYER 01</p></div></aside><main><div class="stage"><h1>A NEW WORLD<br>IS LOADING.</h1><div class="orb"></div></div><div class="newsline">LATEST NEWS / 새로운 모험이 시작됩니다</div><div class="newsline">PLAYER GUIDE / 오늘의 도전 과제</div><div class="newsline">COMMUNITY / 이번 주 플레이 기록</div></main><aside><div class="panel"><h2>FEATURED</h2><p>ORBIT QUEST<br><br>EXPLORE<br>BUILD<br>DISCOVER</p></div><div class="panel"><h2>YOUR STATUS</h2><p>LEVEL 08<br>3 MISSIONS READY</p></div></aside></div>'''
 return f'<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{slug} — 응용 시안</title><style>{base}{css}</style><div class="stamp">FDE DESIGN STUDY / {slug.upper()}-INSPIRED / ORIGINAL LOCAL MOCKUP</div><div class="app">{body}<div class="foot">원본 DESIGN.md를 참고해 새로 구성한 정적 응용 시안 · 공식 제품 화면 아님 · 모든 내용은 예시 데이터</div></div></html>'

def main():
 old=LIB/'token-gallery.html'
 if not old.exists(): old.write_bytes((LIB/'index.html').read_bytes())
 kr=ZipFile(ROOT/'.cache/design-research/korean.zip');gl=ZipFile(ROOT/'.cache/design-research/upstream.zip')
 for f in ['LICENSE','LICENSE-CONTENT','NOTICE']:
  (LIB/('KO-'+f+'.txt')).write_bytes(kr.read('ko-design-md-main/'+f))
 assets=LIB/'screens/assets';assets.mkdir(parents=True,exist_ok=True)
 for n in kr.namelist():
  if n.startswith('ko-design-md-main/public/logos/') and not n.endswith('/'):
   (assets/Path(n).name).write_bytes(kr.read(n))
 (assets/'tokens.css').write_bytes(kr.read('ko-design-md-main/public/preview/_runtime/tokens.css'))
 rows=[]
 for slug,name,kind,character,use,target in KR:
  d=LIB/'screens'/slug;d.mkdir(parents=True,exist_ok=True)
  (d/'DESIGN.md').write_bytes(kr.read(f'ko-design-md-main/services/{slug}.md'))
  raw=kr.read(f'ko-design-md-main/public/preview/{slug}/preview.html').decode()
  write(d/'UPSTREAM.html',raw)
  soup=BeautifulSoup(raw,'html.parser')
  for s in soup.find_all('script'): s.decompose()
  for el in soup.find_all(True):
   for k in list(el.attrs):
    if k.startswith('on'): del el.attrs[k]
   for k in ['src','href']:
    v=el.get(k,'')
    if v.startswith('/logos/'):el[k]='../assets/'+v.split('/')[-1]
    if v=='/preview/_runtime/tokens.css':el[k]='../assets/tokens.css'
  write(d/'preview.html',str(soup))
  sections=soup.select('section')
  chosen=next(x for x in sections if target in x.get_text(' ',strip=True))
  defs='<svg xmlns="http://www.w3.org/2000/svg" style="position:absolute;width:0;height:0;overflow:hidden" aria-hidden="true">'+''.join(str(x) for x in soup.select('defs, svg > symbol'))+'</svg>'
  # Preserve source CSS, select an application region, and label the local adaptation.
  head=str(soup.head)
  screen=f'''<!doctype html><html lang="ko" data-theme="light">{head}<body><div style="font:12px/1.5 system-ui;padding:12px 24px;background:#202020;color:white">{name} · 원본 예시에서 화면 구역을 발췌한 정적 레퍼런스 · 실제 서비스 아님</div>{defs}{chosen}<footer style="font:12px/1.6 system-ui;padding:20px">ko-design-md by ChangSik Yoon · CC BY 4.0 · 원본의 화면 구역 발췌, 스크립트 제거, 로컬 경로 변경. 로고 등은 참고용이며 별도 권리 대상.</footer></body></html>'''
  write(d/'screen.html',screen)
  rows.append(dict(id=slug,name=name,kind=kind,character=character,use=use,region='한국',origin='원본 화면 발췌',source=f'https://www.getdesign.kr/services/{slug}',repo=f'https://github.com/CaesiumY/ko-design-md/blob/main/services/{slug}.md',license='CC BY 4.0 · ChangSik Yoon'))
 for slug,name,kind,character,use in GLOBAL:
  d=LIB/'screens'/slug;d.mkdir(parents=True,exist_ok=True)
  (d/'DESIGN.md').write_bytes(gl.read(f'awesome-design-md-main/design-md/{slug}/DESIGN.md'))
  write(d/'screen.html',global_screen(slug))
  rows.append(dict(id=slug,name=name,kind=kind,character=character,use=use,region='해외',origin='MD 기반 신규 시안',source=f'https://getdesign.md/{slug}/design-md',repo=f'https://github.com/VoltAgent/awesome-design-md/blob/main/design-md/{slug}/DESIGN.md',license='MIT · VoltAgent; 응용 시안은 이 키트에서 작성'))
 order=['baemin','nintendo-2001','greeting','oura','toss','dell-1996','ridi','wired','zigbang','kyobobook','samsung-one-ui','nol']
 rows.sort(key=lambda r:order.index(r['id']))
 for r in rows:
  s=r['id'];p=f'''design-library/COMMON_RULES.md와 design-library/screens/{s}/DESIGN.md, design-library/screens/{s}/APPLY.md를 읽고 화면을 만들어줘. screen.html과 screenshot.png는 정보 구조와 시각적 리듬을 확인하는 참고 자료야. 색만 바꾸지 말고 {r['character']}을 사용자 작업에 맞게 반영해줘. 원 브랜드명·로고·제품 문구는 복제하지 마. 기존 기능을 유지하고 변경 전 백업, 실제 데이터 상태와 모바일 검증, 결과 캡처까지 해줘.'''
  r['prompt']=p
  write(LIB/'screens'/s/'PROMPT.txt',p)
  write(LIB/'screens'/s/'APPLY.md',f'''# {r['name']} · {r['kind']}

{r['character']}. 적합한 용도: {r['use']}.

## 화면의 출처

{r['origin']}. 공식 서비스 화면이 아니라 디자인 분석에 따른 재현 또는 응용 시안이다. 한국 자료는 원본 구역을 발췌하고 스크립트를 제거했으며 로컬 에셋 경로로 바꿨다. 해외 시안은 원본 MD의 색·타이포·구성을 참고해 이 키트에서 새로 작성했다. 정적 예시의 버튼은 제품 기능이 아니다.

![화면 미리보기](screenshot.png)

[화면 열기](screen.html) · [원본 MD](DESIGN.md) · [원본 사이트]({r['source']}) · [GitHub 원본]({r['repo']})

## 적용 기준

- 이 화면의 주 작업을 먼저 정하고 레이아웃·밀도·탐색 방식까지 함께 반영한다.
- 브랜드의 로고·상표·전용 폰트와 더미 문구를 실제 제품 자산으로 복사하지 않는다.
- 한국어 본문 가독성과 키보드 포커스, 빈 값·오류·로딩 상태를 추가한다.
- 원본 MD의 Known Gaps와 추정값을 확인한다. 미리보기는 접근성 합격 증거가 아니다.
- 정적 프리뷰의 작동하지 않는 버튼을 완성 기능으로 설명하지 않는다.

## 출처와 변경 표시

{r['license']}. 확인일 2026-10-26. 한국 자료의 저작자 표시는 ko-design-md by ChangSik Yoon (https://github.com/CaesiumY/ko-design-md), CC BY 4.0. LICENSE-CONTENT와 NOTICE의 제외 항목도 함께 확인한다. 원문 MD는 수정하지 않았다.

## 적용 프롬프트

```text
{p}
```
''')
 write(LIB/'showcase.json',json.dumps(rows,ensure_ascii=False,indent=2))
 cards=[]
 for i,r in enumerate(rows,1):
  s=r['id'];esc=html.escape
  cards.append(f'''<article data-region="{r['region']}" data-search="{esc(' '.join(r[k] for k in ['name','kind','character','use','region']))}"><a class="visual" href="screens/{s}/screen.html" target="_blank"><img src="screens/{s}/screenshot.png" alt="{r['name']} {r['kind']} 화면 예시"><span>{r['origin']} ↗</span></a><div class="caption"><div class="eyebrow">{i:02} / {r['region']} / {r['kind']}</div><h2>{r['name']}<small>{r['character']}</small></h2><p>{r['use']}</p><div class="actions"><a href="screens/{s}/screen.html" target="_blank">화면 크게 보기 ↗</a><a href="screens/{s}/DESIGN.md" download>DESIGN.md ↓</a><a href="screens/{s}/APPLY.md">적용 안내</a><a href="{r['source']}" target="_blank">출처</a><button data-copy="{s}">프롬프트 복사</button></div></div></article>''')
 page='''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>FDE Lookbook — 화면으로 고르는 디자인</title><style>
*{box-sizing:border-box}body{margin:0;background:#eeeee9;color:#191c19;font:15px/1.6 "Malgun Gothic",system-ui,sans-serif}a{color:inherit;text-decoration:none}a:hover{text-decoration:underline}header,main,footer{max-width:1480px;margin:auto;padding:28px 40px}.mast{border-bottom:2px solid #222;display:flex;justify-content:space-between;gap:12px;font:12px monospace;letter-spacing:1px;padding-bottom:18px}.hero{display:grid;grid-template-columns:1.4fr 1fr;gap:40px;padding:42px 0 24px}h1{font-size:clamp(36px,4.5vw,66px);line-height:1.15;letter-spacing:-2.5px;margin:0 0 22px}.hero p{max-width:570px;color:#54594f}.pick{border-left:1px solid #b1b4a9;padding:0 0 0 30px}.pick a{display:block;border-bottom:1px solid #b1b4a9;padding:12px 0}.pick b{font-size:19px}.pick small{display:block;color:#53594f}.toolbar{display:flex;gap:12px;margin-bottom:24px;align-items:center;flex-wrap:wrap}input,select,button{font:inherit;min-height:44px;border:1px solid #aaa;background:transparent;padding:10px 15px;color:#222;border-radius:0}input{flex:1;min-width:180px}button{cursor:pointer}button:hover{background:#d9dfd0}#count{font:12px monospace}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:42px 28px}article{min-width:0}.visual{display:block;aspect-ratio:1.6;background:#ddd;overflow:hidden;position:relative;border:1px solid #c4c6bc}.visual img{width:100%;height:100%;object-fit:cover;object-position:top;display:block}.visual span{position:absolute;bottom:12px;right:12px;background:#fff;color:#222;padding:5px 10px;font-size:11px;border:1px solid #aaa}.caption{padding:18px 0;border-bottom:1px solid #aaa}.eyebrow{font-size:11px;letter-spacing:1px;color:#53594f}h2{font-size:28px;margin:8px 0;line-height:1.4}h2 small{display:block;font-size:15px;font-weight:400}.caption p{color:#53594f;font-size:13px}.actions{display:flex;gap:10px 16px;align-items:center;flex-wrap:wrap;font-size:12px}.actions button{font-size:12px;margin-left:auto}.note{padding:20px 0;border-top:2px solid #222;font-size:13px;color:#53594f}.legacy{display:inline-block;background:#212c23;color:#fff;padding:12px 18px;margin-top:12px}a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible{outline:3px solid #195ac5;outline-offset:3px}dialog{max-width:760px;width:90%;padding:24px;border:1px solid #777}textarea{width:100%;height:240px;font:14px/1.7 monospace}dialog::backdrop{background:#0008}[hidden]{display:none!important}@media(max-width:800px){header,main,footer{padding:22px 18px}.hero,.grid{grid-template-columns:1fr}.pick{border-left:0;padding-left:0}.hero{gap:12px}h1{letter-spacing:-1px}.actions button{margin-left:0}.mast{font-size:10px}.grid{gap:28px}}
</style><header><div class="mast"><b>FDE / DESIGN FIELDNOTES</b><span>VOL.02 — KOREA & GLOBAL</span></div><div class="hero"><div><h1>색상표를 넘어서,<br>화면의 문법을 고르세요.</h1><p>송금 앱, 매물 지도, 채용 콘솔, 책장, 매거진, Y2K 포털.<br>같은 카드의 색만 바꾸는 대신 실제 작업 구조가 다른 12개 화면을 비교합니다.</p><a class="legacy" href="token-gallery.html">기존 토큰 레퍼런스 12종도 보기 ↗</a></div><aside class="pick"><a href="https://www.getdesign.kr/" target="_blank"><b>01 한국 서비스의 화면 문법</b><small>getdesign.kr · 송금 / 탐색 / 채용 / 콘텐츠</small></a><a href="https://getdesign.md/" target="_blank"><b>02 해외 디자인의 표현 범위</b><small>getdesign.md · 편집물 / 웰니스 / 레트로 / 게임</small></a><p>한국 8종은 원본 예시에서 화면 구역을 발췌했습니다. 해외 4종은 공개 MD를 참고해 새로 만든 응용 시안입니다. 모두 공식 제품 스크린샷이 아닌 참고 화면입니다.</p></aside></div></header><main><div class="toolbar"><input id="search" aria-label="디자인 검색" type="search" placeholder="용도나 분위기 검색: 지도, 송금, 레트로, 읽기…"><select id="region" aria-label="지역 분류"><option>전체</option><option>한국</option><option>해외</option></select><span id="count">12 SCREENS</span></div><div class="grid">CARDS</div><p id="empty" hidden>일치하는 화면이 없습니다.</p><p id="status" aria-live="polite"></p></main><footer><div class="note">원본 MD · 화면 예시 · 적용 안내 · 복사할 프롬프트를 각 폴더에 보관했습니다. 화면은 정적 레퍼런스이며 버튼은 제품 기능이 아닙니다. 한국 자료: ko-design-md by ChangSik Yoon, CC BY 4.0 (수정: 화면 구역 발췌·스크립트 제거·로컬 경로). 해외 MD: VoltAgent, MIT. 로고·폰트 등의 권리는 별개입니다. <a href="SHOWCASE.md">출처·변경 내역</a> · <a href="COMMON_RULES.md">공통 적용 기준</a></div></footer><dialog id="prompt"><h2>적용 프롬프트</h2><textarea readonly aria-label="적용 프롬프트"></textarea><button id="close">닫기</button></dialog><script>const data=DATA;const search=document.querySelector('#search'),region=document.querySelector('#region');function filter(){let n=0;for(const c of document.querySelectorAll('article')){c.hidden=!(c.dataset.search.toLowerCase().includes(search.value.toLowerCase())&&(region.value==='전체'||region.value===c.dataset.region));if(!c.hidden)n++}document.querySelector('#count').textContent=n+' SCREENS';document.querySelector('#empty').hidden=n!==0}search.oninput=filter;region.onchange=filter;document.querySelectorAll('[data-copy]').forEach(b=>b.onclick=async()=>{const t=data.find(x=>x.id===b.dataset.copy);try{await navigator.clipboard.writeText(t.prompt);document.querySelector('#status').textContent=t.name+' 프롬프트 복사 완료'}catch{document.querySelector('textarea').value=t.prompt;document.querySelector('#prompt').showModal();document.querySelector('textarea').select()}});document.querySelector('#close').onclick=()=>document.querySelector('#prompt').close();</script></html>'''
 write(LIB/'index.html',page.replace('CARDS',''.join(cards)).replace('DATA',json.dumps(rows,ensure_ascii=False).replace('</','<\\/')))
 print('Screen-first gallery built: 8 Korean excerpts + 4 original global studies.')

if __name__=='__main__':main()
