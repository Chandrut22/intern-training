import type { SocketStatus } from "../types/chat";

const LABELS: Record<SocketStatus, string> = {
  open: "Connected",
  connecting: "Connecting…",
  closed: "Disconnected — retrying",
};

export function ConnectionStatus({ status }: { status: SocketStatus }) {
  return (
    <span>
      <span />
      {LABELS[status]}
    </span>
  );
}