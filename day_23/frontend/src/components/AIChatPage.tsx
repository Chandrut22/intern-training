import { useState } from "react";
import { useChat } from "../hooks/useChat";

export default function AIChatPage() {

  const [message, setMessage] = useState("");

  const [history, setHistory] = useState<
    {
      role: "user" | "assistant";
      text: string;
    }[]
  >([]);

  const chat = useChat();

  async function handleSend() {

    if (!message.trim()) return;

    const text = message;

    setHistory((prev) => [
      ...prev,
      {
        role: "user",
        text,
      },
    ]);

    setMessage("");

    try {

      const response =
        await chat.mutateAsync({
          message: text,
        });

      setHistory((prev) => [
        ...prev,
        {
          role: "assistant",
          text: response.response,
        },
      ]);

    } catch {

      alert("Gemini request failed.");

    }

  }

  return (

    <div className="mx-auto mt-10 max-w-3xl">

      <h1 className="mb-5 text-3xl font-bold">
        Chat Bot
      </h1>

      <div className="mb-5 h-125 overflow-y-auto rounded border p-4">

        {history.map((msg, index) => (

          <div
            key={index}
            className={`mb-4 ${
              msg.role === "user"
                ? "text-right"
                : "text-left"
            }`}
          >

            <div
              className={`inline-block rounded-lg px-4 py-2 ${
                msg.role === "user"
                  ? "bg-blue-500 text-white"
                  : "bg-gray-200"
              }`}
            >

              {msg.text}

            </div>

          </div>

        ))}

      </div>

      <div className="flex gap-2">

        <input
          className="flex-1 rounded border px-4 py-2"
          value={message}
          onChange={(e) =>
            setMessage(e.target.value)
          }
          placeholder="Ask Gemini..."
          onKeyDown={(e) =>
            e.key === "Enter" &&
            handleSend()
          }
        />

        <button
          className="rounded bg-blue-600 px-6 py-2 text-white"
          onClick={handleSend}
          disabled={chat.isPending}
        >
          Send
        </button>

      </div>

    </div>

  );

}