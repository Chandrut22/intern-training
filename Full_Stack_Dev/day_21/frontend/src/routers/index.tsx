import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/")({
  component: () => {
    return (<h1>Welcome to Todo App</h1>);
  }
});
