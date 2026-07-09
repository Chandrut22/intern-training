import { createFileRoute } from "@tanstack/react-router";
import { ChatRoute } from "../components/ChatRoute";

type ChatSearch = {
  sessionId: number;
};

export const Route = createFileRoute("/chat")({
  validateSearch: (search): ChatSearch => ({
    sessionId: Number(search.sessionId ?? 0),
  }),

  component: ChatRoute,
});