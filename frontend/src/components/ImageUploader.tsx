import { useCallback, useId, useRef, useState, type DragEvent } from "react";
import { AlertCircle, ImagePlus, UploadCloud, X } from "lucide-react";

const ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp"];
const MAX_SIZE_BYTES = 15 * 1024 * 1024;

interface Props {
  label: string;
  file: File | null;
  onChange: (file: File | null) => void;
  required?: boolean;
}

export default function ImageUploader({ label, file, onChange, required }: Props) {
  const [dragActive, setDragActive] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const inputId = useId();

  const preview = file ? URL.createObjectURL(file) : null;

  const validateAndSet = useCallback(
    (candidate: File | undefined | null) => {
      if (!candidate) return;
      if (!ALLOWED_TYPES.includes(candidate.type)) {
        setError("Unsupported file type. Please upload a JPG, PNG, or WEBP image.");
        return;
      }
      if (candidate.size > MAX_SIZE_BYTES) {
        setError("File is too large. Maximum size is 15 MB.");
        return;
      }
      setError(null);
      onChange(candidate);
    },
    [onChange]
  );

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragActive(false);
    validateAndSet(e.dataTransfer.files?.[0]);
  };

  const handleRemove = () => {
    onChange(null);
    setError(null);
    if (inputRef.current) inputRef.current.value = "";
  };

  return (
    <div>
      <label htmlFor={inputId} className="mb-2 block text-sm font-medium text-slate-700 dark:text-slate-200">
        {label} {required && <span className="text-rose-500">*</span>}
      </label>

      {!file ? (
        <div
          onDragOver={(e) => {
            e.preventDefault();
            setDragActive(true);
          }}
          onDragLeave={() => setDragActive(false)}
          onDrop={handleDrop}
          className={`flex flex-col items-center justify-center rounded-xl border-2 border-dashed px-6 py-10 text-center transition ${
            dragActive
              ? "border-brand-500 bg-brand-50 dark:bg-brand-500/10"
              : "border-slate-300 hover:border-brand-400 dark:border-white/15"
          }`}
        >
          <UploadCloud className="mb-3 h-8 w-8 text-slate-400" aria-hidden="true" />
          <p className="text-sm text-slate-600 dark:text-slate-300">
            Drag &amp; drop an image, or{" "}
            <button
              type="button"
              className="font-medium text-brand-600 underline-offset-2 hover:underline dark:text-accent-400"
              onClick={() => inputRef.current?.click()}
            >
              browse
            </button>
          </p>
          <p className="mt-1 text-xs text-slate-400">JPG, PNG or WEBP, up to 15MB</p>
          <input
            ref={inputRef}
            id={inputId}
            type="file"
            accept="image/jpeg,image/png,image/webp"
            className="sr-only"
            onChange={(e) => validateAndSet(e.target.files?.[0])}
          />
        </div>
      ) : (
        <div className="relative overflow-hidden rounded-xl border border-slate-200 dark:border-white/10">
          {preview && (
            <img src={preview} alt={`${label} preview`} className="h-48 w-full object-contain bg-slate-100 dark:bg-black/30" />
          )}
          <button
            type="button"
            onClick={handleRemove}
            aria-label={`Remove ${label}`}
            className="absolute right-2 top-2 inline-flex h-7 w-7 items-center justify-center rounded-full bg-black/60 text-white hover:bg-black/80"
          >
            <X className="h-4 w-4" />
          </button>
          <div className="flex items-center gap-2 border-t border-slate-200 bg-white px-3 py-2 text-xs text-slate-500 dark:border-white/10 dark:bg-base-900 dark:text-slate-400">
            <ImagePlus className="h-3.5 w-3.5" />
            <span className="truncate">{file.name}</span>
            <span className="ml-auto">{(file.size / 1024).toFixed(0)} KB</span>
          </div>
        </div>
      )}

      {error && (
        <p role="alert" className="mt-2 flex items-center gap-1.5 text-sm text-rose-600 dark:text-rose-400">
          <AlertCircle className="h-4 w-4" /> {error}
        </p>
      )}
    </div>
  );
}
