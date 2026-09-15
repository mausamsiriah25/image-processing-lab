import { useEffect, useState } from "react";
import { fetchPracticalDetail, fetchPracticals } from "../services/practicalService";
import { ApiError } from "../services/api";
import type { PracticalDetail, PracticalSummary } from "../types/practical";

interface AsyncState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
}

export function usePracticalList() {
  const [state, setState] = useState<AsyncState<PracticalSummary[]>>({
    data: null,
    loading: true,
    error: null,
  });

  useEffect(() => {
    let cancelled = false;
    setState({ data: null, loading: true, error: null });
    fetchPracticals()
      .then((res) => {
        if (!cancelled) setState({ data: res.practicals, loading: false, error: null });
      })
      .catch((err: unknown) => {
        if (!cancelled) {
          const message = err instanceof ApiError ? err.message : "Failed to load practicals.";
          setState({ data: null, loading: false, error: message });
        }
      });
    return () => {
      cancelled = true;
    };
  }, []);

  return state;
}

export function usePracticalDetail(id: string | undefined) {
  const [state, setState] = useState<AsyncState<PracticalDetail>>({
    data: null,
    loading: true,
    error: null,
  });

  useEffect(() => {
    if (!id) return;
    let cancelled = false;
    setState({ data: null, loading: true, error: null });
    fetchPracticalDetail(id)
      .then((res) => {
        if (!cancelled) setState({ data: res, loading: false, error: null });
      })
      .catch((err: unknown) => {
        if (!cancelled) {
          const message = err instanceof ApiError ? err.message : "Failed to load this practical.";
          setState({ data: null, loading: false, error: message });
        }
      });
    return () => {
      cancelled = true;
    };
  }, [id]);

  return state;
}
