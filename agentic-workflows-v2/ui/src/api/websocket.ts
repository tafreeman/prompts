import type { ExecutionEvent } from "./types";

export type EventHandler = (event: ExecutionEvent) => void;

/**
 * Creates a WebSocket connection to the execution stream for a run.
 * Automatically reconnects on disconnect (up to maxRetries).
 */
export function connectExecutionStream(
  runId: string,
  onEvent: EventHandler,
  options: { maxRetries?: number; retryDelayMs?: number } = {}
): { close: () => void } {
  const { maxRetries = 5, retryDelayMs = 1000 } = options;
  let ws: WebSocket | null = null;
  let retries = 0;
  let closed = false;

  function connect() {
    if (closed) return;

    const protocol = location.protocol === "https:" ? "wss:" : "ws:";
    ws = new WebSocket(`${protocol}//${location.host}/ws/execution/${runId}`);

    ws.onopen = () => {
      retries = 0;
    };

    ws.onmessage = (evt) => {
      try {
        const event = JSON.parse(evt.data) as ExecutionEvent;
        onEvent(event);
      } catch {
        // ignore parse errors
      }
    };

    ws.onclose = () => {
      if (closed) return;
      if (retries < maxRetries) {
        retries++;
        setTimeout(connect, retryDelayMs * retries);
      }
    };

    ws.onerror = () => {
      ws?.close();
    };
  }

  connect();

  return {
    close() {
      closed = true;
      ws?.close();
    },
  };
}
