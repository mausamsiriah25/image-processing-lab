import { apiPostJsonForBlob } from "./api";
import type { ProcessingResult, StudentInfo } from "../types/processing";

export async function generateReport(
  practicalId: string,
  studentInfo: StudentInfo,
  result: ProcessingResult,
  inputImages: Record<string, string>
): Promise<Blob> {
  return apiPostJsonForBlob(`/api/practicals/${practicalId}/report`, {
    studentInfo,
    result,
    inputImages,
  });
}

export function downloadBlob(blob: Blob, filename: string): void {
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}
