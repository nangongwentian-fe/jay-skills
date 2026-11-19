// Evaluation stub: records an attempted project start; never opens a server.
import { appendFileSync } from 'node:fs';
appendFileSync('start-attempts.log','dev invoked\n');
console.log('Evaluation preview service is unavailable');
