import { useQuery } from "@tanstack/react-query";
import { getTodoById } from "../api/todo";
import { getRouteApi, Link } from "@tanstack/react-router";

const routeApi = getRouteApi("/tasks/$taskId/");

export function TaskDetails() {
  const { taskId } = routeApi.useParams();

  const { data, isLoading, isError } = useQuery({
    queryKey: ["task", taskId],
    queryFn: () => getTodoById(Number(taskId)),
  });

  if (isLoading) {
    return (
      <div className="flex h-32 items-center justify-center">
        <h2 className="text-sm font-medium text-gray-500 animate-pulse">Loading details...</h2>
      </div>
    );
  }

  if (isError || !data) {
    return (
      <div className="max-w-md p-4 text-center">
        <h2 className="text-sm font-medium text-red-600 bg-red-50 border border-red-200 rounded-md p-3">
          Task details not found
        </h2>
      </div>
    );
  }

  return (
    <div className="max-w-md bg-white border border-gray-200 rounded-lg p-6 shadow-sm space-y-5">
      {/* Header with Title and Status Badge */}
      <div className="flex items-start justify-between gap-4">
        <h1 className="text-xl font-bold text-gray-900 tracking-tight">
          {data.task_title}
        </h1>
        <span 
          className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium border ${
            data.iscompleted 
              ? "bg-green-50 text-green-700 border-green-200" 
              : "bg-amber-50 text-amber-700 border-amber-200"
          }`}
        >
          {data.iscompleted ? "Completed" : "Pending"}
        </span>
      </div>

      {/* Description Text Box */}
      <div>
        <h3 className="text-xs font-medium text-gray-400 uppercase tracking-wider mb-1">
          Description
        </h3>
        <p className="text-sm text-gray-600 bg-gray-50 rounded-md p-3 border border-gray-100 whitespace-pre-wrap min-h-24">
          {data.description || <span className="italic text-gray-400">No description provided.</span>}
        </p>
      </div>

      {/* Action Navigation Footer */}
      <div className="pt-2 border-t border-gray-100 flex items-center justify-between gap-4 text-sm">
        <Link 
          to="/tasks"
          className="text-gray-500 hover:text-black transition-colors"
        >
          ← Back to Tasks
        </Link>
        
        <Link 
          to="/tasks/$taskId/edit"
          params={{ taskId }}
          className="bg-black hover:bg-gray-800 text-white font-medium px-4 py-1.5 rounded-md transition-colors text-xs"
        >
          Edit Task
        </Link>
      </div>
    </div>
  );
}
