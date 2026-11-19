import {test} from 'node:test'; import assert from 'node:assert/strict'; import {readFileSync} from 'node:fs';
test('preserves save action',()=>assert.match(readFileSync('Panel.jsx','utf8'),/保存/));
