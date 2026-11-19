export async function resume(checkpoint, tools) {
  if (checkpoint.done) return checkpoint.result;
  const result = await tools.createTicket({ title: checkpoint.title });
  await tools.checkpoint({ ...checkpoint, done: true, result });
  return result;
}
