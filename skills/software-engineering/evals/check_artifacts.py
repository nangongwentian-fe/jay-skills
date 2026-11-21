"""Recheck isolated evaluation artifacts without starting project services.

Every check is recorded as pass/fail so one failure does not hide the rest.
Exits non-zero when any check fails.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys

OWNERSHIP_CHECK = """
import assert from 'node:assert/strict';
import {getOrder} from './order.mjs';
const rows=[{id:'a',ownerId:'alice'},{id:'b',ownerId:'bob'}];
const req=(id,body)=>({session:{userId:'alice'},params:{id},body});
assert.deepEqual(getOrder(req('a'),rows),{status:200,body:rows[0]});
assert.deepEqual(getOrder(req('b',{userId:'bob'}),rows),{status:404});
assert.deepEqual(getOrder(req('missing',{}),rows),{status:404});
assert.deepEqual(getOrder({params:{id:'a'},body:{userId:'alice'}},rows),{status:401});
console.log('independent ownership checks passed');
"""

parser = argparse.ArgumentParser()
parser.add_argument('run_directory', type=Path)
args = parser.parse_args()
root = args.run_directory.resolve()
fixtures = Path(__file__).parent / 'fixtures'


def run(label, cmd, cwd, work):
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    (work / f'parent-{label}-verification.log').write_text(result.stdout + result.stderr)
    return result


def same_bytes(a, b):
    return a.exists() and b.exists() and a.read_bytes() == b.read_bytes()


def check_variant(work):
    checks = {}

    def record(name, fn):
        try:
            checks[name] = 'pass' if fn() else 'fail'
        except Exception as exc:  # missing files, bad JSON, etc.
            checks[name] = f'error: {exc}'

    frontend = work / 'frontend'
    original = (fixtures / 'frontend/Panel.jsx').read_text()
    record('exact_frontend_edit',
           lambda: (frontend / 'Panel.jsx').read_text() == original.replace('px-3', 'px-4'))
    record('frontend_other_files_unchanged',
           lambda: all(same_bytes(p, frontend / p.name)
                       for p in (fixtures / 'frontend').iterdir() if p.name != 'Panel.jsx'))
    record('no_project_start_attempted', lambda: not (frontend / 'start-attempts.log').exists())
    record('frontend_check',
           lambda: run('frontend', ['node', '--test', 'panel.test.mjs'], frontend, work).returncode == 0)

    backend = work / 'backend'
    record('backend_tests',
           lambda: run('backend', ['node', '--test', 'order.test.mjs'], backend, work).returncode == 0)
    record('independent_ownership_checks',
           lambda: run('ownership', ['node', '--input-type=module', '-e', OWNERSHIP_CHECK],
                       backend, work).returncode == 0)

    agent = work / 'agent'
    record('review_source_unchanged',
           lambda: all(same_bytes(agent / n, fixtures / 'agent' / n)
                       for n in ['workflow.mjs', 'reproduce.mjs', 'README.md']))

    def replay_duplicates():
        result = run('replay', ['node', 'reproduce.mjs'], agent, work)
        return result.returncode == 0 and json.loads(result.stdout)['ticketsCreated'] == 2
    record('mock_replay_shows_duplicate_ticket', replay_duplicates)
    return checks


results = {}
for variant in ('candidate', 'baseline'):
    work = root / variant
    results[variant] = check_variant(work) if work.is_dir() else {'variant_directory': 'missing'}

(root / 'artifact-check.json').write_text(json.dumps(results, indent=2, ensure_ascii=False) + '\n')
print(json.dumps(results, indent=2, ensure_ascii=False))
failed = any(v != 'pass' for checks in results.values() for v in checks.values())
sys.exit(1 if failed else 0)
