import { useCallback } from "react";
import useWebSocket from "react-use-websocket"
import { ReadyState } from "react-use-websocket";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import type { ChatMessage, ServerEvent, SocketStatus } from "../types/chat";

// import * as ReactUseWebSocketModule from "react-use-websocket";
// type UseWebSocketHook = typeof import("react-use-websocket").default;

// const resolveUseWebSocket = (mod: unknown): UseWebSocketHook => {
//   const m = mod as { default?: { default?: unknown } };
//   const candidate = m.default?.default ?? m.default ?? mod;
//   if (typeof candidate !== "function") {
//     throw new Error(
//       "react-use-websocket could not be resolved — try restarting Vite with `npm run dev -- --force`"
//     );
//   }
//   return candidate as UseWebSocketHook;
// };



// const useWebSocket = resolveUseWebSocket(ReactUseWebSocketModule);




// eslint-disable-next-line @typescript-eslint/no-explicit-any
const useWs = (useWebSocket as any).default as typeof useWebSocket



const WS_BASE = import.meta.env.VITE_WS_URL ?? "ws://127.0.0.1:8000";

const chatKey = (sessionId: number) => ["chat", sessionId] as const;


const STATUS_MAP: Record<ReadyState, SocketStatus> = {
  [ReadyState.CONNECTING]: "connecting",
  [ReadyState.OPEN]: "open",
  [ReadyState.CLOSING]: "closed",
  [ReadyState.CLOSED]: "closed",
  [ReadyState.UNINSTANTIATED]: "closed",
};

export function useChatSocket(sessionId: number) {
  const queryClient = useQueryClient();

  const token = localStorage.getItem("access_token");

  const socketUrl =
    token && sessionId > 0
      ? `${WS_BASE}/chat/${sessionId}?token=${token}`
      : null;

  const { sendMessage: sendRaw, readyState } = useWs(socketUrl, {

    onMessage: (event: MessageEvent<string>) => {
      const data: ServerEvent = JSON.parse(event.data);

      if (data.type === "history") {
        queryClient.setQueryData<ChatMessage[]>(
          chatKey(sessionId),
          data.messages
        );
      } else if (data.type === "message") {
        const { user_id, message, created_at } = data;
        queryClient.setQueryData<ChatMessage[]>(
          chatKey(sessionId),
          (old = []) => [...old, { user_id, message, created_at }]
        );
      }
    },

    shouldReconnect: () => true,
    reconnectInterval: 2000,
    reconnectAttempts: 20,
  });

  const { data: messages = [] } = useQuery<ChatMessage[]>({
    queryKey: chatKey(sessionId),
    queryFn: () =>
      queryClient.getQueryData<ChatMessage[]>(chatKey(sessionId)) ?? [],
    staleTime: Infinity,
    gcTime: Infinity,
  });

  const status: SocketStatus = STATUS_MAP[readyState];

  const sendMessage = useCallback(
    (text: string) => {
      const trimmed = text.trim();
      if (!trimmed || readyState !== ReadyState.OPEN) return false;
      sendRaw(trimmed);
      return true;
    },
    [sendRaw, readyState]
  );

  return { messages, status, sendMessage };
}
