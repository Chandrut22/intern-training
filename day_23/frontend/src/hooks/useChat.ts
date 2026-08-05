import { useMutation } from "@tanstack/react-query";
import { sendMessage } from "../api/ai";

export function useChat() {
  return useMutation({
    mutationFn: sendMessage,
  });
}