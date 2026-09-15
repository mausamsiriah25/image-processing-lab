import { apiGet } from "./api";
import type { PracticalDetail, PracticalListResponse } from "../types/practical";

export async function fetchPracticals(): Promise<PracticalListResponse> {
  return apiGet<PracticalListResponse>("/api/practicals");
}

export async function fetchPracticalDetail(id: string): Promise<PracticalDetail> {
  return apiGet<PracticalDetail>(`/api/practicals/${id}`);
}
