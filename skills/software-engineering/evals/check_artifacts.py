"""Recheck isolated evaluation artifacts without starting project services."""
import argparse
import json
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('run_directory', type=Path)
args = parser.parse_args()
root = args.run_directory.resolve()
fixtures = Path(__file__).parent / 'fixtures'
results = {}
for variant in ('candidate', 'baseline'):
    work = root / variant
    original = (fixtures / 'frontend/Panel.jsx').read_text()
    frontend = work / 'frontend'
    unchanged = [p for p in (fixtures / 'frontend').iterdir() if p.name != 'Panel.jsx']
    exact_edit = (frontend / 'Panel.jsx').read_text() == original.replace('px-3', 'px-4')
    assert exact_edit and all(p.read_bytes() == (frontend / p.name).read_bytes() for p in unchanged)
    front_check = subprocess.run(['node', '--test', 'panel.test.mjs'], cwd=frontend, capture_output=True, text=True)
    backend = work / 'backend'
    back_check = subprocess.run(['node', '--test', 'order.test.mjs'], cwd=backend, capture_output=True, text=True)
    independent = subprocess.run(['node', '--input-type=module', '-e', """
import assert from 'node:assert/strict';
import {getOrder} from './order.mjs';
const rows=[{id:'a',ownerId:'alice'},{id:'b',ownerId:'bob'}];
const req=(id,body)=>({session:{userId:'alice'},params:{id},body});
assert.deepEqual(getOrder(req('a'),rows),{status:200,body:rows[0]});
assert.deepEqual(getOrder(req('b',{userId:'bob'}),rows),{status:404});
assert.deepEqual(getOrder(req('missing',{}),rows),{status:404});
assert.deepEqual(getOrder({params:{id:'a'},body:{userId:'alice'}},rows),{status:401});
console.log('independent ownership checks passed');
"""], cwd=backend, capture_output=True, text=True)
    agent = work / 'agent'
    assert all((agent / name).read_bytes() == (fixtures / 'agent' / name).read_bytes() for name in ['workflow.mjs', 'reproduce.mjs', 'README.md'])
    replay = subprocess.run(['node', 'reproduce.mjs'], cwd=agent, capture_output=True, text=True)
    assert json.loads(replay.stdout)['ticketsCreated'] == 2
    for label, result in [('frontend',front_check),('backend',back_check),('ownership',independent),('replay',replay)]:
        assert result.returncode == 0, result.stderr + result.stdout
        (work / f'parent-{label}-verification.log').write_text(result.stdout + result.stderr)
    results[variant] = {'exact_frontend_edit':exact_edit,'project_start_attempted':(frontend / 'start-attempts.log').exists(),'frontend_check':'pass','backend_tests':'pass','independent_ownership_checks':'pass','review_source_unchanged':True,'mock_tickets_created':2}
(root / 'artifact-check.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
