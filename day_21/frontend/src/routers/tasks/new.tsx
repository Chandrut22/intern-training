import { createFileRoute } from "@tanstack/react-router";
import CreateTask from "../../components/CreateTask";

export const Route = createFileRoute("/tasks/new")({
  component: CreateTask,
});

