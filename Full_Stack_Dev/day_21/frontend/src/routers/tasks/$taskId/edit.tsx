import { createFileRoute } from "@tanstack/react-router";
import { EditTask } from "../../../components/EditTask";

export const Route = createFileRoute("/tasks/$taskId/edit")({
  component: EditTask,
});
