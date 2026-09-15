import { useState } from "react";
import { X, FileDown, Loader2, AlertCircle } from "lucide-react";
import type { ProcessingResult, StudentInfo } from "../types/processing";
import { downloadBlob, generateReport } from "../services/reportService";
import { ApiError } from "../services/api";

interface Props {
  open: boolean;
  onClose: () => void;
  practicalId: string;
  result: ProcessingResult;
  inputImages: Record<string, string>;
}

const EMPTY_STUDENT: StudentInfo = {
  name: "",
  rollNumber: "",
  usn: "",
  semester: "",
  section: "",
  date: new Date().toISOString().slice(0, 10),
};

type Status = "idle" | "generating" | "success" | "error";

export default function ReportDialog({ open, onClose, practicalId, result, inputImages }: Props) {
  const [student, setStudent] = useState<StudentInfo>(EMPTY_STUDENT);
  const [status, setStatus] = useState<Status>("idle");
  const [error, setError] = useState<string | null>(null);

  if (!open) return null;

  const handleChange = (key: keyof StudentInfo, value: string) => {
    setStudent((prev) => ({ ...prev, [key]: value }));
  };

  const handleGenerate = async () => {
    if (!student.name.trim()) {
      setError("Student name is required.");
      return;
    }
    setStatus("generating");
    setError(null);
    try {
      const blob = await generateReport(practicalId, student, result, inputImages);
      downloadBlob(blob, `${practicalId}-report.pdf`);
      setStatus("success");
    } catch (err) {
      const message = err instanceof ApiError ? err.message : "Report generation failed. Please try again.";
      setError(message);
      setStatus("error");
    }
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4"
      role="dialog"
      aria-modal="true"
      aria-labelledby="report-dialog-title"
    >
      <div className="w-full max-w-lg rounded-2xl border border-slate-200 bg-white p-6 dark:border-white/10 dark:bg-base-900">
        <div className="mb-4 flex items-center justify-between">
          <h2 id="report-dialog-title" className="text-lg font-semibold">
            Generate Report
          </h2>
          <button
            type="button"
            onClick={onClose}
            aria-label="Close dialog"
            className="rounded-lg p-1 text-slate-400 hover:bg-slate-100 dark:hover:bg-white/10"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        <div className="grid grid-cols-2 gap-3">
          <label className="col-span-2 text-sm">
            <span className="mb-1 block text-slate-600 dark:text-slate-300">Student Name *</span>
            <input
              value={student.name}
              onChange={(e) => handleChange("name", e.target.value)}
              className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm dark:border-white/15 dark:bg-base-950"
            />
          </label>
          <label className="text-sm">
            <span className="mb-1 block text-slate-600 dark:text-slate-300">Roll Number</span>
            <input
              value={student.rollNumber}
              onChange={(e) => handleChange("rollNumber", e.target.value)}
              className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm dark:border-white/15 dark:bg-base-950"
            />
          </label>
          <label className="text-sm">
            <span className="mb-1 block text-slate-600 dark:text-slate-300">USN</span>
            <input
              value={student.usn}
              onChange={(e) => handleChange("usn", e.target.value)}
              className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm dark:border-white/15 dark:bg-base-950"
            />
          </label>
          <label className="text-sm">
            <span className="mb-1 block text-slate-600 dark:text-slate-300">Semester</span>
            <input
              value={student.semester}
              onChange={(e) => handleChange("semester", e.target.value)}
              className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm dark:border-white/15 dark:bg-base-950"
            />
          </label>
          <label className="text-sm">
            <span className="mb-1 block text-slate-600 dark:text-slate-300">Section</span>
            <input
              value={student.section}
              onChange={(e) => handleChange("section", e.target.value)}
              className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm dark:border-white/15 dark:bg-base-950"
            />
          </label>
          <label className="col-span-2 text-sm">
            <span className="mb-1 block text-slate-600 dark:text-slate-300">Date</span>
            <input
              type="date"
              value={student.date}
              onChange={(e) => handleChange("date", e.target.value)}
              className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm dark:border-white/15 dark:bg-base-950"
            />
          </label>
        </div>

        {error && (
          <p role="alert" className="mt-3 flex items-center gap-1.5 text-sm text-rose-600 dark:text-rose-400">
            <AlertCircle className="h-4 w-4" /> {error}
          </p>
        )}

        {status === "success" && (
          <p className="mt-3 text-sm text-emerald-600 dark:text-emerald-400">
            Report downloaded. You can generate it again if needed.
          </p>
        )}

        <div className="mt-5 flex justify-end gap-2">
          <button
            type="button"
            onClick={onClose}
            className="rounded-lg px-4 py-2 text-sm font-medium text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-white/10"
          >
            Cancel
          </button>
          <button
            type="button"
            onClick={handleGenerate}
            disabled={status === "generating"}
            className="inline-flex items-center gap-2 rounded-lg bg-brand-600 px-4 py-2 text-sm font-semibold text-white transition hover:bg-brand-700 disabled:opacity-60"
          >
            {status === "generating" ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <FileDown className="h-4 w-4" />
            )}
            {status === "generating" ? "Generating…" : "Generate PDF"}
          </button>
        </div>
      </div>
    </div>
  );
}
