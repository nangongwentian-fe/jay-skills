import {resume} from './workflow.mjs';
const tickets=[];let first=true;
const tools={createTicket:async input=>{tickets.push(input);return {id:tickets.length};},checkpoint:async()=>{if(first){first=false;throw Error('checkpoint unavailable');}}};
const state={actionId:'action-1',title:'test',done:false};
try {await resume(state,tools);} catch {}
await resume(state,tools);
console.log(JSON.stringify({ticketsCreated:tickets.length}));
