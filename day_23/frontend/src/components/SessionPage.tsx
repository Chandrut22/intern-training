import { useState } from "react";
import { useNavigate } from "@tanstack/react-router";
import { useCurrentUser } from "../hooks/useCurrentUser";

export default function SessionPage() {
  const navigate = useNavigate();

  const { data: user, isLoading } = useCurrentUser();

  const [sessionId, setSessionId] = useState("");

  const [error, setError] = useState("");

  function handleChatBot(){
    navigate({
      to: "/chatbot",
    });
  }

  function handleJoin() {
    const sid = Number(sessionId);

    if (!Number.isInteger(sid) || sid <= 0) {
      setError("Enter a valid Session ID");
      return;
    }

    setError("");

    navigate({
      to: "/chat",
      search: {
        sessionId: sid,
      },
    });
  }

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gray-100">
        <h2 className="text-xl font-semibold text-gray-700">
          Loading...
        </h2>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-100">
      <div className="w-full max-w-md rounded-lg bg-white p-8 shadow-lg">
        <h1 className="mb-2 text-center text-3xl font-bold text-gray-800">
          Join Chat Session
        </h1>

        <p className="mb-6 text-center text-gray-600">
          Welcome, <span className="font-semibold">{user?.username}</span>
        </p>

        <div className="space-y-4">
          <input
            type="number"
            placeholder="Enter Session ID"
            value={sessionId}
            onChange={(e) => setSessionId(e.target.value)}
            className="w-full rounded-md border border-gray-300 px-4 py-2 outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
          />

          {error && (
            <p className="text-sm text-red-600">
              {error}
            </p>
          )}

          <button
            onClick={handleJoin}
            className="w-full rounded-md bg-blue-600 py-2 font-medium text-white transition hover:bg-blue-700"
          >
            Join Session
          </button>
        </div>
        <button
            onClick={handleChatBot}
            className="w-full rounded-md bg-blue-600 py-2 font-medium text-white transition hover:bg-blue-700"
          >
            Or AI ChatBot
          </button>
      </div>
    </div>
  );
}