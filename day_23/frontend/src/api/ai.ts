import api from "./client";
import type {
  ChatRequest,
  ChatResponse,
} from "../types/chat";

export async function sendMessage(
  data: ChatRequest
): Promise<ChatResponse> {

  const response =
    await api.post<ChatResponse>(
      "/chat",
      data
    );

  return response.data;
}