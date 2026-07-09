import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useNavigate } from "@tanstack/react-router";
import { createTodo } from "../api/todo";

export default function CreateTask() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const is_competed : boolean = false;

  const createMutation = useMutation({
    mutationFn: createTodo,
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["tasks"],
      });
      navigate({
        to: "/tasks",
      });
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    createMutation.mutate({
      title,
      description,
      is_competed,
    });
  };

  return (
    <div className="max-w-md bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
      {/* Title Header */}
      <h1 className="text-xl font-bold text-gray-900 mb-6">Create Task</h1>

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Title Input Field */}
        <div>
          <label className="block text-xs font-medium text-gray-600 mb-1">
            Title
          </label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Enter the Title"
            required
            className="w-full text-sm px-3 py-2 border border-gray-300 rounded-md outline-none transition-all placeholder:text-gray-400 focus:border-black focus:ring-1 focus:ring-black"
          />
        </div>

        {/* Description Input Field */}
        <div>
          <label className="block text-xs font-medium text-gray-600 mb-1">
            Description
          </label>
          <textarea
            value={description}
            placeholder="Enter the description"
            onChange={(e) => setDescription(e.target.value)}
            rows={5}
            required
            className="w-full text-sm px-3 py-2 border border-gray-300 rounded-md outline-none transition-all placeholder:text-gray-400 focus:border-black focus:ring-1 focus:ring-black resize-none"
          />
        </div>

        {/* Create Submit Action Element */}
        <button
          type="submit"
          disabled={createMutation.isPending}
          className="w-full text-sm bg-black hover:bg-gray-800 text-white font-medium py-2 rounded-md transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed shadow-sm"
        >
          {createMutation.isPending ? "Creating..." : "Create Task"}
        </button>
      </form>

      {/* Failure Error Alert Banner */}
      {createMutation.isError && (
        <p className="mt-4 text-xs text-red-600 bg-red-50 border border-red-100 rounded-md p-2 text-center">
          Error:{" "}
          {createMutation.error instanceof Error
            ? createMutation.error.message
            : "Something went wrong"}
        </p>
      )}
    </div>
  );
}
