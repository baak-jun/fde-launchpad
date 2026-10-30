"""Offline FDE preparation kit. No dependencies, API keys, installation or deployment."""
import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def read(name):
    return json.loads((ROOT / 'catalog' / name).read_text(encoding='utf-8'))

def scaffold(recipe_id, name, work_root=None):
    if not re.fullmatch(r'[a-z0-9][a-z0-9_-]{0,63}', name):
        raise ValueError('Name must be 1-64 lowercase ASCII letters/digits/-/_, starting with letter/digit')
    if name.split('.')[0].upper() in {'CON','PRN','AUX','NUL',*(f'COM{i}' for i in range(10)),*(f'LPT{i}' for i in range(10))}:
        raise ValueError('Reserved Windows name')
    recipe = next((r for r in read('recipes.json') if r['id'] == recipe_id), None)
    if recipe is None:
        raise ValueError('Unknown recipe: ' + recipe_id)
    base = Path(work_root) if work_root else ROOT / 'work'
    base.mkdir(parents=True, exist_ok=True)
    dest = base / name
    dest.mkdir(exist_ok=False)
    (dest / 'recipe.json').write_text(json.dumps(recipe, indent=2, ensure_ascii=False), encoding='utf-8')
    brief = (ROOT / 'templates/BRIEF.md').read_text(encoding='utf-8')
    brief = brief.replace('{{PROJECT}}', name).replace('{{RECIPE}}', recipe['name']).replace('{{FIRST_SLICE}}', recipe['first_slice'])
    (dest / 'BRIEF.md').write_text(brief, encoding='utf-8')
    for filename in ['EVALUATION.json', 'DEMO.md', 'ADAPTER_CONTRACT.json', 'COST.json', 'IMPLEMENTATION_PROMPT.txt', 'INTENT.md', 'UNDERSTANDING.md']:
        (dest / filename).write_bytes((ROOT / 'templates' / filename).read_bytes())
    return dest


def start_project(name, work_root=None):
    """Copy a self-contained source starter, without environments, keys or user data."""
    dest = scaffold('triage', name, work_root)
    folders = ['runtime','domain_packs','catalog','templates','examples','tests','scripts','docs','evidence','skills','design-library','.devcontainer']
    for folder in folders:
        shutil.copytree(ROOT / folder, dest / folder, ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    for filename in ['kit.py','run_workbench.py','launch.cmd','requirements.in','requirements.lock','.gitignore','README.md']:
        shutil.copy2(ROOT / filename, dest / filename)
    (dest/'HANDOFF.md').write_text((ROOT/'templates/HANDOFF.md').read_text(encoding='utf-8').replace('{{PROJECT}}',name),encoding='utf-8')
    return dest


def prepare(profile_id, name, work_root=None, fetch=False):
    """Generate a launch packet; optionally fetch upstream without executing its code."""
    profile = next((p for p in read('launchpads.json') if p['id'] == profile_id), None)
    if profile is None:
        raise ValueError('Unknown launchpad: ' + profile_id)
    dest = start_project(name, work_root) if profile_id == 'local' else scaffold(profile['recipe'], name, work_root)
    (dest / 'launchpad.json').write_text(json.dumps(profile, ensure_ascii=False, indent=2), encoding='utf-8')
    for filename in ['HANDOFF.md']:
        (dest / filename).write_text((ROOT / 'templates' / filename).read_text(encoding='utf-8').replace('{{PROJECT}}', name), encoding='utf-8')
    lines = [f'# {name} 시작하기', '', profile['name'], '', profile['when'], '', '## 순서', '']
    lines += [f'{i}. {step}' for i, step in enumerate(profile['steps'], 1)]
    lines += ['', '## 기반 저장소', '', profile['url'] or '현재 로컬 키트', '', '## 범위와 조건', '', profile['limit'], '', '## 공통 완료 기준', '',
              '- BRIEF.md와 INTENT.md에 실제 문제·제약·완료 조건을 적습니다.',
              '- 정상·권한 거부·실패/재시도 사례를 검증합니다.',
              '- UNDERSTANDING.md에 구조와 실패 지점을 설명하고 HANDOFF.md에 상태를 남깁니다.',
              '- 외부 저장소는 별도 앱입니다. 현재 승인 엔진과 자동 통합되지는 않습니다.',
              '- 디자인은 원본 키트 design-library에서 하나를 골라 DESIGN.md와 COMMON_RULES.md를 프로젝트에 복사합니다.']
    if profile['url']:
        lines += ['', '## 원본 코드 가져오기', '', '이 폴더에서 실행하세요. 설치·서버 실행은 원본 README를 따릅니다.', '', '```powershell',
                  f"git clone --depth 1 {profile['url']}.git upstream", 'git -C upstream rev-parse HEAD', '```', '',
                  '이미 --fetch로 가져왔다면 다시 clone하지 마세요. 가져온 커밋은 UPSTREAM_COMMIT.txt에 기록됩니다.']
    (dest / 'START_HERE.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    if fetch and profile['url']:
        subprocess.run(['git', 'clone', '--depth', '1', profile['url'] + '.git', str(dest / 'upstream')], check=True)
        commit = subprocess.check_output(['git', '-C', str(dest / 'upstream'), 'rev-parse', 'HEAD'], text=True).strip()
        (dest / 'UPSTREAM_COMMIT.txt').write_text(commit + '\n', encoding='utf-8')
    return dest

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('recipes', help='List eight problem recipes')
    sub.add_parser('choose', help='Choose a starting base by problem type')
    launch = sub.add_parser('prepare', help='Create a launch packet; --fetch clones upstream but does not install or run it')
    launch.add_argument('profile', choices=[p['id'] for p in read('launchpads.json')])
    launch.add_argument('name')
    launch.add_argument('--fetch', action='store_true')
    find = sub.add_parser('find', help='Search curated repositories without network')
    find.add_argument('query')
    new = sub.add_parser('new', help='Create a planning packet, not a runnable application')
    new.add_argument('recipe', choices=[r['id'] for r in read('recipes.json')])
    new.add_argument('name')
    demo = sub.add_parser('demo', help='Run a small reusable capability with synthetic inputs')
    demo.add_argument('name', choices=['documents','analytics','planner','recommendation'])
    start = sub.add_parser('start', help='Copy a runnable source starter; no dependencies, credentials or runtime data copied')
    start.add_argument('name')
    args = parser.parse_args()
    if args.command == 'choose':
        for p in read('launchpads.json'):
            print(f"{p['id']:12} {p['name']}\n  {p['when']}\n  python kit.py prepare {p['id']} my-project\n")
    elif args.command == 'prepare':
        print(prepare(args.profile, args.name, fetch=args.fetch))
        print('Read START_HERE.md. External bases require their own installation and integration.')
    elif args.command == 'recipes':
        for recipe in read('recipes.json'):
            print(f'{recipe["id"]:16} {recipe["name"]}: {recipe["first_slice"]}')
    elif args.command == 'find':
        matches = [r for r in read('repos.json') if args.query.casefold() in json.dumps({k:r[k] for k in ['repo','category','use_when','tags']}, ensure_ascii=False).casefold()]
        for row in matches:
            print(row['repo'], '-', row['use_when'], '\n ', row['url'], '\n ', row['license_summary'], '|', row['caveat'])
        extra = [p for p in read('launchpads.json') if p['url'] and p['url'] not in {r['url'] for r in matches}
                 and args.query.casefold() in json.dumps(p, ensure_ascii=False).casefold()]
        for p in extra:
            print(p['url'], '-', p['when'], '\n ', p['limit'], '\n ', f"python kit.py prepare {p['id']} my-project")
        if not matches and not extra:
            print('No match. Try document, data, workflow, mobile, audio, schedule, crud.')
    elif args.command == 'demo':
        from runtime.capabilities import run
        print(json.dumps(run(args.name), indent=2, ensure_ascii=False))
    elif args.command == 'start':
        print(start_project(args.name))
        print('Source starter created. Run scripts/setup.ps1, then scripts/verify.py in the new directory.')
    else:
        print(scaffold(args.recipe, args.name))
        print('Planning templates only. Fill TODOs and integrate the selected repositories before claiming an app is ready.')

if __name__ == '__main__':
    main()
