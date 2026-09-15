import { apiPostForm } from "./api";
import type { ProcessingResult } from "../types/processing";

export interface ProcessRequestImages {
  image?: File | null;
  image2?: File | null;
  template?: File | null;
  target?: File | null;
}

export async function runExperiment(
  practicalId: string,
  images: ProcessRequestImages,
  params: Record<string, unknown>
): Promise<ProcessingResult> {
  const formData = new FormData();
  formData.append("params", JSON.stringify(params));
  if (images.image) formData.append("image", images.image);
  if (images.image2) formData.append("image2", images.image2);
  if (images.template) formData.append("template", images.template);
  if (images.target) formData.append("target", images.target);

  return apiPostForm<ProcessingResult>(`/api/practicals/${practicalId}/process`, formData);
}
