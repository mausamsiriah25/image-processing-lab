/**
 * Centralized fetch wrapper. Every request to the backend goes through here
 * so base URL, error shape, and timeouts are handled in exactly one place.
 */
import type { ApiErrorPayload } from "../types/processing";

const BASE_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
const DEFAULT_TIMEOUT_MS = 30_000;

export class ApiError extends Error {
  code: string;
  status: number;

  constructor(message: string, code: string, status: number) {
    super(message);
    this.name = "ApiError";
    this.code = code;
    this.status = status;
  }
}

async function withTimeout<T>(promise: Promise<T>, ms: number): Promise<T> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), ms);
  try {
    return await promise;
  } finally {
    clearTimeout(timer);
  }
}

async function parseErrorResponse(response: Response): Promise<never> {
  let payload: ApiErrorPayload | null = null;
  try {
    payload = await response.json();
  } catch {
    // response body wasn't JSON — fall through to generic message
  }
  const detail = (payload as { error?: { code: string; message: string } } | null)?.error;
  throw new ApiError(
    detail?.message ?? "The server returned an unexpected error. Please try again.",
    detail?.code ?? "UNKNOWN_ERROR",
    response.status
  );
}

export async function apiGet<T>(path: string): Promise<T> {
  let response: Response;
  try {
    response = await withTimeout(fetch(`${BASE_URL}${path}`), DEFAULT_TIMEOUT_MS);
  } catch {
    throw new ApiError("Could not reach the backend. Is it running?", "NETWORK_ERROR", 0);
  }
  if (!response.ok) await parseErrorResponse(response);
  return response.json();
}

export async function apiPostForm<T>(path: string, formData: FormData): Promise<T> {
  let response: Response;
  try {
    response = await withTimeout(
      fetch(`${BASE_URL}${path}`, { method: "POST", body: formData }),
      DEFAULT_TIMEOUT_MS
    );
  } catch {
    throw new ApiError("Could not reach the backend. Is it running?", "NETWORK_ERROR", 0);
  }
  if (!response.ok) await parseErrorResponse(response);
  return response.json();
}

export async function apiPostJsonForBlob(path: string, body: unknown): Promise<Blob> {
  let response: Response;
  try {
    response = await withTimeout(
      fetch(`${BASE_URL}${path}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      }),
      DEFAULT_TIMEOUT_MS
    );
  } catch {
    throw new ApiError("Could not reach the backend. Is it running?", "NETWORK_ERROR", 0);
  }
  if (!response.ok) await parseErrorResponse(response);
  return response.blob();
}
