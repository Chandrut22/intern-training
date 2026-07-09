import { createFileRoute, redirect } from "@tanstack/react-router";
import SessionPage from "../components/SessionPage";

export const Route = createFileRoute("/session")({
  beforeLoad: () => {
    const token = localStorage.getItem("access_token");
      if (!token) {
        throw redirect({
              to: "/login",
          });
        }
  },
  component: SessionPage,
});