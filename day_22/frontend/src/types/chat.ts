export interface ChatMessage {
  user_id: number;
  message: string;
  created_at: string; // ISO string from datetime.isoformat()
}

/** Everything the FastAPI server can push over the socket. */
export type ServerEvent =
  | { type: "history"; messages: ChatMessage[] }
  | ({ type: "message" } & ChatMessage);

export type SocketStatus = "connecting" | "open" | "closed";