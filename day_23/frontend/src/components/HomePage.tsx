import { Link } from "@tanstack/react-router";

export default function HomePage() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-100">
      <div className="w-full max-w-md rounded-lg bg-white p-8 shadow-lg">
        <h1 className="mb-8 text-center text-3xl font-bold text-gray-800">
          Chat Application
        </h1>

        <div className="flex flex-col gap-4">
          <Link
            to="/login"
            className="rounded-md bg-blue-600 px-4 py-3 text-center font-medium text-white transition hover:bg-blue-700"
          >
            Login
          </Link>

          <Link
            to="/register"
            className="rounded-md bg-green-600 px-4 py-3 text-center font-medium text-white transition hover:bg-green-700"
          >
            Register
          </Link>
        </div>
      </div>
    </div>
  );
}