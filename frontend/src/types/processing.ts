export type OutputType = "image" | "chart" | "value" | "table";

export interface ProcessingOutput {
  name: string;
  type: OutputType;
  data: unknown;
  caption?: string | null;
  filename?: string | null;
}

export interface ProcessingResult {
  success: boolean;
  processingTime: number;
  outputs: ProcessingOutput[];
  metadata: Record<string, unknown>;
  warnings: string[];
  error?: string | null;
}

export interface ApiErrorPayload {
  error: {
    code: string;
    message: string;
  };
}

export interface StudentInfo {
  name: string;
  rollNumber: string;
  usn: string;
  semester: string;
  section: string;
  date: string;
}
