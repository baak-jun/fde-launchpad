"""Build the readable catalog from reviewed metadata. Network-free."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def build():
    path = ROOT / 'catalog/repos.json'
    rows = json.loads(path.read_text(encoding='utf-8'))
    evidence = json.loads((ROOT / 'evidence/research.json').read_text(encoding='utf-8'))
    lookup = {x['repo']: x for x in evidence}
    lookup.update({x.get('canonical_repo'): x for x in evidence})
    overrides = {
        'vercel/ai': 'Apache-2.0', 'pgvector/pgvector': 'PostgreSQL License',
        'activepieces/activepieces': 'MIT core; EE separate',
        'langfuse/langfuse': 'MIT core; EE separate',
        'medusajs/medusa': 'MIT core; Enterprise separate',
        'n8n-io/n8n': 'Sustainable Use License; EE separate',
        'langgenius/dify': 'Dify license (Apache-2.0 + additional conditions)',
    }
    for row in rows:
        item = lookup[row['repo']]
        row['source_repo'] = item['repo']
        row['repo'] = item.get('canonical_repo', row['repo'])
        row['url'] = 'https://github.com/' + row['repo']
        row['license_summary'] = overrides.get(row['repo'], (item.get('license_api') or {}).get('spdx_id', 'unverified'))
        row['checked_at_utc'] = item['checked_at_utc']
        row['last_push_utc'] = item.get('pushed_at')
        row['archived'] = item.get('archived')
        row['readme_url'] = item.get('readme_url')
        row['license_url'] = item.get('license_url')
        row['verification'] = 'Official README, metadata and root license checked; runtime not tested' if item.get('license_url') else 'Official README and metadata checked; license file retrieval pending; runtime not tested'
        if row['repo'] == 'calcom/cal.diy':
            row.update(tier='도메인베이스', caveat='MIT Cal.diy; 기존 cal.com 링크가 이 저장소로 이동. 팀·조직·SSO 등 EE 기능 제거; 상용 Cal.com과 구분')
        if row['repo'] == 'medusajs/medusa':
            row['caveat'] = 'MIT core와 Enterprise 코드 분리; 결제·배송·세금은 별도 통합'
    path.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    lines = ['# 문제별 오픈소스 후보 28개', '', '조사 기준일: 2026-10-26 KST. 공식 README·GitHub 메타데이터·루트 LICENSE 기반. 모든 후보의 앱 실행은 미검증이다. 기본은 우선 학습 후보라는 뜻이며 모두 설치하라는 뜻은 아니다.', '', '## 빠른 비교', '', '| 문제 | 후보 | 선택 시점 | 구분 | 라이선스 요약 |', '|---|---|---|---|---|']
    for row in rows:
        lines.append(f'| {row["category"]} | [{row["repo"]}]({row["url"]}) | {row["use_when"]} | {row["tier"]} | {row["license_summary"]} |')
    lines += ['', '## 선택 시 확인할 점', '', '라이선스 표는 루트 파일의 분류다. 실제 가져갈 커밋·하위 패키지·모델·데이터의 조건과 고지 파일을 함께 확인한다. 최종 제품 전체의 이용 가능성을 이 표만으로 판단하지 않는다. last push는 유지보수의 단서이며 품질·보안 보증이나 최신 릴리스 날짜가 아니다.', '']
    for row in rows:
        lines += [f'### {row["repo"]}', '', row['caveat'], '', f'- 최근 push UTC: {row["last_push_utc"]}; archived: {row["archived"]}', f'- [공식 README]({row["readme_url"]}) · [루트 라이선스]({row["license_url"]})', f'- 로컬 증거: `evidence/github/{row["source_repo"].replace("/", "__")}/`', '']
    (ROOT / 'docs/REPOSITORIES.md').write_text('\n'.join(lines), encoding='utf-8')

if __name__ == '__main__':
    build()
