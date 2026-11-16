import { readFileSync } from 'node:fs';
import { test } from 'node:test';
import assert from 'node:assert/strict';
const html = readFileSync(new URL('./index.html', import.meta.url), 'utf8');
test('retains task controls', () => { for (const text of ['任务步骤', 'name="taskName"', '下一步']) assert.ok(html.includes(text)); });
