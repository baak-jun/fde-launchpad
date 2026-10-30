"""Refresh official GitHub metadata and cache README/license evidence, without installation."""
import concurrent.futures
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def fetch(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'fde-kit-research', 'Accept': 'application/vnd.github+json'})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()

def inspect(row):
    repo = row['repo']
    folder = ROOT / 'evidence' / 'github' / repo.replace('/', '__')
    folder.mkdir(parents=True, exist_ok=True)
    result = {'repo': repo, 'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'runtime_tested': False}
    try:
        info = json.loads(fetch(f'https://api.github.com/repos/{repo}'))
        branch = info['default_branch']
        result.update(canonical_repo=info['full_name'], archived=info['archived'], pushed_at=info['pushed_at'], default_branch=branch, license_api=info.get('license'), description=info['description'])
        for kind, candidates in [('readme', ['README.md', 'readme.md', 'README.rst']), ('license', ['LICENSE', 'LICENSE.md', 'LICENSE.txt', 'LICENSE-MIT', 'license.txt'])]:
            errors = []
            for filename in candidates:
                url = f'https://raw.githubusercontent.com/{info["full_name"]}/{branch}/{filename}'
                try:
                    data = fetch(url)
                    (folder / f'{kind}.txt').write_bytes(data)
                    result[kind + '_url'] = url
                    break
                except Exception as exc:
                    errors.append(type(exc).__name__ + ': ' + str(exc))
            else:
                result[kind + '_errors'] = errors
    except Exception as exc:
        result['error'] = type(exc).__name__ + ': ' + str(exc)
    (folder / 'metadata.json').write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
    return result

if __name__ == '__main__':
    rows = json.loads((ROOT / 'catalog/repos.json').read_text(encoding='utf-8'))
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(inspect, rows))
    (ROOT / 'evidence/research.json').write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding='utf-8')
    for result in results:
        license_info = result.get('license_api') or {}
        print(result['repo'], license_info.get('spdx_id'), 'archived=' + str(result.get('archived')), 'readme=' + str('readme_url' in result), 'license=' + str('license_url' in result), result.get('error', ''))
