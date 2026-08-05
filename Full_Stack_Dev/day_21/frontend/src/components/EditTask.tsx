import { getRouteApi, useNavigate } from "@tanstack/react-router";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { getTodoById, updateTodo } from "../api/todo";

export type Todo = {
  id: number;
  task_title: string;
  description: string;
  iscompleted: boolean;
};

export type UpdateTaskPayload = {
  title: string;
  description: string;
  is_competed: boolean; 
};

const routeApi = getRouteApi("/tasks/$taskId/edit");

export function EditTask() {
  const { taskId } = routeApi.useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const { data, isLoading, isError } = useQuery<Todo>({
    queryKey: ["task", taskId],
    queryFn: () => getTodoById(Number(taskId)),
  });

  const mutation = useMutation({
    mutationFn: (payload: UpdateTaskPayload) => updateTodo(Number(taskId), payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["tasks"] });
      queryClient.invalidateQueries({ queryKey: ["task", taskId] });
      navigate({ to: "/tasks" });
    },
  });

  if (isLoading) {
    return (
      <div className="flex h-32 items-center justify-center">
        <h2 className="text-sm font-medium text-gray-500 animate-pulse">Loading task...</h2>
      </div>
    );
  }

  if (isError || !data) {
    return (
      <div className="max-w-md p-4 text-center">
        <h2 className="text-sm font-medium text-red-600 bg-red-50 border border-red-200 rounded-md p-3">
          Task not found
        </h2>
      </div>
    );
  }

  function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();

    const formData = new FormData(e.currentTarget);
    const title = formData.get("title") as string;
    const description = formData.get("description") as string;
    const isCompleted = formData.get("completed") === "on";

    mutation.mutate({
      title,
      description,
      is_competed: isCompleted, 
    });
  }

  return (
    <div className="max-w-md bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
      {/* Title Header */}
      <h1 className="text-xl font-bold text-gray-900 mb-6">Edit Task</h1>

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Title Input Field */}
        <div>
          <label htmlFor="title" className="block text-xs font-medium text-gray-600 mb-1">
            Title
          </label>
          <input
            id="title"
            name="title"
            type="text"
            defaultValue={data.task_title}
            placeholder="Enter the title"
            required
            className="w-full text-sm px-3 py-2 border border-gray-300 rounded-md outline-none transition-all placeholder:text-gray-400 focus:border-black focus:ring-1 focus:ring-black"
          />
        </div>

        {/* Description Input Field */}
        <div>
          <label htmlFor="description" className="block text-xs font-medium text-gray-600 mb-1">
            Description
          </label>
          <textarea
            id="description"
            name="description"
            rows={4}
            defaultValue={data.description}
            placeholder="Enter the description"
            className="w-full text-sm px-3 py-2 border border-gray-300 rounded-md outline-none transition-all placeholder:text-gray-400 focus:border-black focus:ring-1 focus:ring-black resize-none"
          />
        </div>

        {/* Completed Checkbox */}
        <div className="pt-1">
          <label className="inline-flex items-center gap-2 cursor-pointer text-sm font-medium text-gray-700 select-none">
            <input
              name="completed"
              type="checkbox"
              defaultChecked={data.iscompleted}
              className="w-4 h-4 rounded border-gray-300 text-black focus:ring-black cursor-pointer accent-black"
            />
            Completed
          </label>
        </div>

        {/* Action Buttons */}
        <div className="pt-2 flex flex-col gap-2">
          <button
            type="submit"
            disabled={mutation.isPending}
            className="w-full text-sm bg-black hover:bg-gray-800 text-white font-medium py-2 rounded-md transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed shadow-sm"
          >
            {mutation.isPending ? "Updating..." : "Update Task"}
          </button>
          
          <button
            type="button"
            onClick={() => navigate({ to: "/tasks" })}
            className="w-full text-sm bg-transparent hover:bg-gray-50 text-gray-600 font-medium py-2 border border-gray-200 rounded-md transition-colors"
          >
            Cancel
          </button>
        </div>
      </form>

      {/* Global Error Banner */}
      {mutation.isError && (
        <p className="mt-4 text-xs font-medium text-red-600 bg-red-50 border border-red-100 rounded-md p-2 text-center">
          Failed to update the task. Please try again.
        </p>
      )}
    </div>
  );
}
