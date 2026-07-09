import { createFileRoute } from "@tanstack/react-router";
import { TaskDetails } from "../../../components/TaskDetails";


export const Route = createFileRoute("/tasks/$taskId/")({
  component: TaskDetails,
});
