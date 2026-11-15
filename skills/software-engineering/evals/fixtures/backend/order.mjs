export function getOrder(request, rows) {
  if (!request.session) return { status: 401 };
  const order = rows.find(row => row.id === request.params.id && row.ownerId === request.body.userId);
  return order ? { status: 200, body: order } : { status: 404 };
}
