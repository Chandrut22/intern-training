import { useQuery } from "@tanstack/react-query";
import { getTodos, deleteTodo } from "../api/todo";
import { useMutation } from "@tanstack/react-query";
import { queryClient } from "../main"
import { Link } from "@tanstack/react-router";



export function TasksPage() {

    const deleteMutation = useMutation({
      mutationFn: deleteTodo,
      onSuccess: () => {
          queryClient.invalidateQueries({
          queryKey: ["tasks"],
          });
      },
    });

    const { data, isLoading, isError } = useQuery({
        queryKey: ["tasks"],
        queryFn: getTodos,
    });

    if (isLoading) return <h2 className="text-sm font-medium text-gray-500 animate-pulse">Loading...</h2>;

    if (isError) return <h2 className="text-sm font-medium text-red-600 bg-red-50 border border-red-200 rounded-md p-3 max-w-md">Error loading tasks</h2>;

    

  return (
    <div className="max-w-2xl space-y-6">
      <h1 className="text-xl font-bold text-gray-900 border-b border-gray-100 pb-3">Tasks</h1>

      {data?.map((task) => (
        <div className="bg-white border border-gray-200 rounded-lg p-5 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4 transition-colors hover:bg-gray-50/50"
          key={task.id}
        >
          <div className="space-y-1">
            <h3 className="text-sm font-semibold tracking-tight text-gray-900">{task.title}</h3>

            <p className="text-xs text-gray-500 line-clamp-2">{task.description}</p>
          </div>

          <div className="flex items-center gap-3 text-xs font-medium border-t pt-3 sm:border-t-0 sm:pt-0 border-gray-100">
            <Link
              to="/tasks/$taskId"
              params={{ taskId: String(task.id) }}
              className="text-gray-500 hover:text-black transition-colors"
            >
              View
            </Link>

            <span className="text-gray-200">|</span>

            <Link
              to="/tasks/$taskId/edit"
              params={{ taskId: String(task.id) }}
              className="text-gray-500 hover:text-black transition-colors"
            >
              Edit
            </Link>
            
            <span className="text-gray-200">|</span>
            
            <button
                onClick={() => deleteMutation.mutate(task.id)}
                className="text-red-500 hover:text-red-700 disabled:text-gray-300 transition-colors cursor-pointer"
              >
                Delete
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}
