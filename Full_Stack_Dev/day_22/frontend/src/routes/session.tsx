import { createFileRoute } from "@tanstack/react-router";
import SessionPage from "../components/SessionPage";

export const Route = createFileRoute("/session")({
  component: SessionPage,
});