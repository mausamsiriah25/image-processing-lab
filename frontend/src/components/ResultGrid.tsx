import { Download } from "lucide-react";
import type { ProcessingOutput } from "../types/processing";
import { downloadDataUrl } from "../utils/format";

interface Props {
  outputs: ProcessingOutput[];
}

function ImageCard({ output, index }: { output: ProcessingOutput; index: number }) {
  const src = String(output.data);
  const filename = output.filename ?? `output-${index + 1}.png`;
  return (
    <div className="overflow-hidden rounded-xl border border-slate-200 bg-white dark:border-white/10 dark:bg-white/5">
      <img src={src} alt={output.name} className="h-56 w-full bg-slate-100 object-contain dark:bg-black/30" />
      <div className="flex items-center justify-between gap-2 border-t border-slate-200 px-3 py-2 dark:border-white/10">
        <div className="min-w-0">
          <p className="truncate text-sm font-medium text-slate-700 dark:text-slate-200">{output.name}</p>
          {output.caption && <p className="truncate text-xs text-slate-400">{output.caption}</p>}
        </div>
        <button
          type="button"
          onClick={() => downloadDataUrl(src, filename)}
          aria-label={`Download ${output.name}`}
          className="inline-flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-lg border border-slate-200 text-slate-500 hover:border-brand-400 hover:text-brand-600 dark:border-white/10 dark:text-slate-300"
        >
          <Download className="h-4 w-4" />
        </button>
      </div>
    </div>
  );
}

function ValueCard({ output }: { output: ProcessingOutput }) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-4 dark:border-white/10 dark:bg-white/5">
      <p className="text-xs font-medium uppercase tracking-wide text-slate-400">{output.name}</p>
      <p className="mt-1 text-2xl font-semibold text-brand-600 dark:text-accent-400">{String(output.data)}</p>
      {output.caption && <p className="mt-1 text-xs text-slate-400">{output.caption}</p>}
    </div>
  );
}

function TableCard({ output }: { output: ProcessingOutput }) {
  const rows = (output.data as Record<string, unknown>[]) ?? [];
  const headers = rows.length > 0 ? Object.keys(rows[0]) : [];
  return (
    <div className="col-span-full overflow-hidden rounded-xl border border-slate-200 bg-white dark:border-white/10 dark:bg-white/5">
      <p className="border-b border-slate-200 px-4 py-2 text-sm font-medium text-slate-700 dark:border-white/10 dark:text-slate-200">
        {output.name}
      </p>
      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm">
          <thead className="bg-slate-50 text-xs uppercase text-slate-500 dark:bg-white/5 dark:text-slate-400">
            <tr>
              {headers.map((h) => (
                <th key={h} scope="col" className="px-4 py-2 font-medium">
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row, i) => (
              <tr key={i} className="border-t border-slate-100 dark:border-white/5">
                {headers.map((h) => (
                  <td key={h} className="px-4 py-2 text-slate-600 dark:text-slate-300">
                    {String(row[h])}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {output.caption && <p className="px-4 py-2 text-xs text-slate-400">{output.caption}</p>}
    </div>
  );
}

export default function ResultGrid({ outputs }: Props) {
  if (outputs.length === 0) return null;

  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {outputs.map((output, i) => {
        if (output.type === "image" || output.type === "chart") {
          return <ImageCard key={`${output.name}-${i}`} output={output} index={i} />;
        }
        if (output.type === "value") {
          return <ValueCard key={`${output.name}-${i}`} output={output} />;
        }
        return <TableCard key={`${output.name}-${i}`} output={output} />;
      })}
    </div>
  );
}
