import { Route } from "../routes/chat";
import { ChatPage } from "./ChatPage";

export function ChatRoute() {
  const { sessionId } = Route.useSearch();

  if (!Number.isInteger(sessionId) || sessionId <= 0) {
    return <h2>Invalid Session</h2>;
  }

  return <ChatPage sessionId={sessionId} />;
}