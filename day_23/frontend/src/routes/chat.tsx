import { createFileRoute, redirect } from "@tanstack/react-router";
import { ChatRoute } from "../components/ChatRoute";

type ChatSearch = {
  sessionId: number;
};

export const Route = createFileRoute("/chat")({
  beforeLoad: () => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      throw redirect({
              to: "/login",
          });
      }
    },
  validateSearch: (search): ChatSearch => ({
    sessionId: Number(search.sessionId ?? 0),
  }),

  component: ChatRoute,
});