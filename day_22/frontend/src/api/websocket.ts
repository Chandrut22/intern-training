export const getWebSocketUrl = (
    sessionId: string,
    userId: string | number
) =>
    `ws://localhost:8000/chat/${sessionId}?user_id=${userId}`;