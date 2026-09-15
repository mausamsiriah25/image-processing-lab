export type PracticalType = "practical" | "postlab";

export interface ParameterOption {
  value: string;
  label: string;
}

export interface ParameterSpec {
  key: string;
  label: string;
  type: "slider" | "number" | "select" | "radio" | "checkbox";
  min?: number;
  max?: number;
  step?: number;
  default: string | number | boolean;
  options?: ParameterOption[];
}

export interface PracticalSummary {
  id: string;
  number: number;
  type: PracticalType;
  title: string;
  category: string;
  aim: string;
  requiresImage: boolean;
  multiImage: boolean;
}

export interface PracticalDetail extends PracticalSummary {
  objectives: string[];
  theory: string;
  algorithm: string[];
  referenceCode: string;
  syntax: string[];
  parameters: ParameterSpec[];
  expectedOutputs: string[];
  observation: string;
  conclusion: string;
  postLab: string[];
}

export interface PracticalListResponse {
  practicals: PracticalSummary[];
  total: number;
}
