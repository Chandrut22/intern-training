import { createRootRoute, Link, Outlet } from "@tanstack/react-router";

export const Route = createRootRoute({
  component: () => {
    return (
      <div className="max-w-2xl mx-auto px-6 py-8 font-sans antialiased text-gray-800">
        <nav className="flex gap-8 mb-6 text-sm">
          <Link 
            to="/" 
            className="text-gray-500 hover:text-black transition-colors"
            activeProps={{ className: "text-black font-semibold" }}
          >
            Home
          </Link>

          <Link 
            to="/tasks" 
            className="text-gray-500 hover:text-black transition-colors"
            activeProps={{ className: "text-black font-semibold" }}
          >
            Tasks
          </Link>

          <Link 
            to="/tasks/new" 
            className="text-gray-500 hover:text-black transition-colors"
            activeProps={{ className: "text-black font-semibold" }}
          >
            Create Task
          </Link>
        </nav>

        <div className="border-b border-gray-200 mb-8" />

        <main>
          <Outlet />
        </main>
      </div>
    );
  }
});
