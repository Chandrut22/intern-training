import { useEffect, useRef, useState } from "react";
import { Link } from "@tanstack/react-router";
import { useChatSocket } from "../hooks/useChatSocket";
import { ConnectionStatus } from "./ConnectionStatus";
import { useCurrentUser } from "../hooks/useCurrentUser";

interface ChatPageProps {
  sessionId: number;
}

export function ChatPage({ sessionId }: ChatPageProps) {
  const { messages, status, sendMessage } = useChatSocket(sessionId);

  const { data: currentUser } = useCurrentUser();

  const [draft, setDraft] = useState("");

  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages.length]);

  function handleSend() {
    if (sendMessage(draft)) {
      setDraft("");
    }
  }

  return (
    <div className="flex h-screen flex-col bg-gray-100">
      {/* Header */}
      <header className="flex items-center justify-between border-b bg-white px-6 py-4 shadow">
        <div>
          <h1 className="text-2xl font-bold text-gray-800">
            Session #{sessionId}
          </h1>

          <p className="text-sm text-gray-500">
            {currentUser
              ? `You are ${currentUser.username}`
              : "Loading user..."}
          </p>
        </div>

        <div className="flex items-center gap-4">
          <ConnectionStatus status={status} />

          <Link
            to="/"
            className="rounded-md bg-red-500 px-4 py-2 text-white transition hover:bg-red-600"
          >
            Leave
          </Link>
        </div>
      </header>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-6">
        {messages.length === 0 ? (
          <p className="text-center text-gray-500">
            {status === "open"
              ? "No messages in this session yet. Say hello."
              : "Loading..."}
          </p>
        ) : (
          <div className="space-y-4">
            {messages.map((msg, index) => {
              const mine = msg.user_id === currentUser?.id;

              return (
                <div
                  key={`${msg.created_at}-${index}`}
                  className={`max-w-md rounded-lg px-4 py-3 shadow ${
                    mine
                      ? "ml-auto bg-blue-500 text-white"
                      : "mr-auto bg-white"
                  }`}
                >
                  {!mine && (
                    <div className="mb-1 text-xs font-semibold text-gray-600">
                      User {msg.user_id}
                    </div>
                  )}

                  <div>{msg.message}</div>

                  <div
                    className={`mt-2 text-xs ${
                      mine
                        ? "text-blue-100"
                        : "text-gray-500"
                    }`}
                  >
                    {new Date(msg.created_at).toLocaleTimeString([], {
                      hour: "2-digit",
                      minute: "2-digit",
                    })}
                  </div>
                </div>
              );
            })}
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div className="border-t bg-white p-4">
        <div className="flex gap-3">
          <input
            className="flex-1 rounded-md border border-gray-300 px-4 py-2 outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
            value={draft}
            onChange={(e) => setDraft(e.target.value)}
            onKeyDown={(e) =>
              e.key === "Enter" && handleSend()
            }
            placeholder="Type a message..."
            disabled={status !== "open"}
          />

          <button
            onClick={handleSend}
            disabled={
              status !== "open" ||
              !draft.trim()
            }
            className="rounded-md bg-blue-600 px-6 py-2 font-medium text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-gray-400"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}