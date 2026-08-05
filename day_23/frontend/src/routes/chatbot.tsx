import { createFileRoute, redirect } from "@tanstack/react-router";
import AIChatPage from "../components/AIChatPage";

export const Route =
  createFileRoute("/chatbot")({
    beforeLoad: () => {
        const token = localStorage.getItem("access_token");

        if (!token) {
        throw redirect({
            to: "/login",
        });
        }
    },
    component: AIChatPage,
  });