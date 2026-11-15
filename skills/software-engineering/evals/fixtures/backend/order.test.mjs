import { test } from 'node:test'; import assert from 'node:assert/strict'; import { getOrder } from './order.mjs';
test('guest denied',()=>assert.equal(getOrder({params:{id:'1'},body:{}},[]).status,401));
