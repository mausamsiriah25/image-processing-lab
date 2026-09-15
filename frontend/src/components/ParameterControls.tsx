import type { ParameterSpec } from "../types/practical";

interface Props {
  parameters: ParameterSpec[];
  values: Record<string, string | number | boolean>;
  onChange: (key: string, value: string | number | boolean) => void;
  onReset: () => void;
}

export default function ParameterControls({ parameters, values, onChange, onReset }: Props) {
  if (parameters.length === 0) return null;

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-5 dark:border-white/10 dark:bg-white/5">
      <div className="mb-4 flex items-center justify-between">
        <h3 className="text-sm font-semibold text-slate-700 dark:text-slate-200">Parameters</h3>
        <button
          type="button"
          onClick={onReset}
          className="text-xs font-medium text-brand-600 hover:underline dark:text-accent-400"
        >
          Reset to defaults
        </button>
      </div>

      <div className="grid gap-5 sm:grid-cols-2">
        {parameters.map((param) => {
          const value = values[param.key] ?? param.default;
          const inputId = `param-${param.key}`;

          if (param.type === "select") {
            return (
              <div key={param.key}>
                <label htmlFor={inputId} className="mb-1.5 block text-xs font-medium text-slate-500 dark:text-slate-400">
                  {param.label}
                </label>
                <select
                  id={inputId}
                  value={String(value)}
                  onChange={(e) => onChange(param.key, e.target.value)}
                  className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm dark:border-white/15 dark:bg-base-900"
                >
                  {param.options?.map((opt) => (
                    <option key={opt.value} value={opt.value}>
                      {opt.label}
                    </option>
                  ))}
                </select>
              </div>
            );
          }

          if (param.type === "slider") {
            return (
              <div key={param.key}>
                <label htmlFor={inputId} className="mb-1.5 flex justify-between text-xs font-medium text-slate-500 dark:text-slate-400">
                  <span>{param.label}</span>
                  <span className="font-mono text-slate-700 dark:text-slate-200">{String(value)}</span>
                </label>
                <input
                  id={inputId}
                  type="range"
                  min={param.min}
                  max={param.max}
                  step={param.step ?? 1}
                  value={Number(value)}
                  onChange={(e) => onChange(param.key, Number(e.target.value))}
                  className="w-full accent-brand-600"
                />
              </div>
            );
          }

          if (param.type === "checkbox") {
            return (
              <div key={param.key} className="flex items-center gap-2">
                <input
                  id={inputId}
                  type="checkbox"
                  checked={Boolean(value)}
                  onChange={(e) => onChange(param.key, e.target.checked)}
                  className="h-4 w-4 rounded border-slate-300 text-brand-600"
                />
                <label htmlFor={inputId} className="text-sm text-slate-600 dark:text-slate-300">
                  {param.label}
                </label>
              </div>
            );
          }

          // number / radio fallback to a numeric input
          return (
            <div key={param.key}>
              <label htmlFor={inputId} className="mb-1.5 block text-xs font-medium text-slate-500 dark:text-slate-400">
                {param.label}
              </label>
              <input
                id={inputId}
                type="number"
                min={param.min}
                max={param.max}
                step={param.step ?? 1}
                value={Number(value)}
                onChange={(e) => onChange(param.key, Number(e.target.value))}
                className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm dark:border-white/15 dark:bg-base-900"
              />
            </div>
          );
        })}
      </div>
    </div>
  );
}
