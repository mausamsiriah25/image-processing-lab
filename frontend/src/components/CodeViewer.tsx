import { useMemo, useState, type ReactNode } from "react";
import { Check, Copy, Maximize2, Minimize2 } from "lucide-react";

interface Props {
  code: string;
  label?: string;
}

/**
 * Lightweight Python syntax highlighter. We intentionally avoid pulling in a
 * heavyweight highlighting library — the token set needed for classroom
 * OpenCV/NumPy code is small and this keeps the bundle light.
 */
const KEYWORDS = new Set([
  "import", "from", "as", "if", "elif", "else", "for", "while", "def", "return",
  "class", "try", "except", "finally", "with", "raise", "pass", "break", "continue",
  "in", "is", "not", "and", "or", "None", "True", "False", "lambda", "global",
]);

function highlightLine(line: string): ReactNode[] {
  const tokens = line.split(/(\s+|[()[\]{}.,:=+\-*/<>%]|"[^"]*"|'[^']*')/g).filter((t) => t !== "");
  return tokens.map((token, i) => {
    if (/^#/.test(token)) {
      return (
        <span key={i} className="text-slate-500">
          {token}
        </span>
      );
    }
    if (/^["'].*["']$/.test(token)) {
      return (
        <span key={i} className="text-emerald-400">
          {token}
        </span>
      );
    }
    if (KEYWORDS.has(token)) {
      return (
        <span key={i} className="text-fuchsia-400 font-medium">
          {token}
        </span>
      );
    }
    if (/^\d+(\.\d+)?$/.test(token)) {
      return (
        <span key={i} className="text-amber-400">
          {token}
        </span>
      );
    }
    if (/^(cv2|np|plt|cv)\./.test(token) || /^(cv2|np|plt)$/.test(token)) {
      return (
        <span key={i} className="text-sky-400">
          {token}
        </span>
      );
    }
    return <span key={i}>{token}</span>;
  });
}

function stripFence(code: string): string {
  return code
    .trim()
    .replace(/^```[a-zA-Z]*\n?/, "")
    .replace(/```$/, "")
    .trimEnd();
}

export default function CodeViewer({ code, label = "Python" }: Props) {
  const [copied, setCopied] = useState(false);
  const [expanded, setExpanded] = useState(false);
  const cleanCode = useMemo(() => stripFence(code), [code]);
  const lines = useMemo(() => cleanCode.split("\n"), [cleanCode]);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(cleanCode);
      setCopied(true);
      setTimeout(() => setCopied(false), 1800);
    } catch {
      // Clipboard API can fail in insecure contexts; fail silently, UI already
      // indicates non-success by not flipping `copied`.
    }
  };

  return (
    <div
      className={`overflow-hidden rounded-xl border border-slate-800 bg-[#0b0f19] text-sm text-slate-200 ${
        expanded ? "fixed inset-4 z-50 flex flex-col" : "relative"
      }`}
    >
      <div className="flex items-center justify-between border-b border-slate-800 bg-[#0d1220] px-4 py-2">
        <div className="flex items-center gap-2">
          <span className="h-2.5 w-2.5 rounded-full bg-red-500/70" />
          <span className="h-2.5 w-2.5 rounded-full bg-amber-500/70" />
          <span className="h-2.5 w-2.5 rounded-full bg-emerald-500/70" />
          <span className="ml-2 text-xs font-medium text-slate-400">{label}</span>
        </div>
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={handleCopy}
            className="inline-flex items-center gap-1 rounded-md px-2 py-1 text-xs text-slate-300 hover:bg-white/5"
          >
            {copied ? <Check className="h-3.5 w-3.5 text-emerald-400" /> : <Copy className="h-3.5 w-3.5" />}
            {copied ? "Copied" : "Copy"}
          </button>
          <button
            type="button"
            onClick={() => setExpanded((v) => !v)}
            aria-label={expanded ? "Exit fullscreen" : "View fullscreen"}
            className="inline-flex items-center rounded-md px-2 py-1 text-xs text-slate-300 hover:bg-white/5"
          >
            {expanded ? <Minimize2 className="h-3.5 w-3.5" /> : <Maximize2 className="h-3.5 w-3.5" />}
          </button>
        </div>
      </div>
      <div className={`overflow-auto ${expanded ? "flex-1" : "max-h-[420px]"}`}>
        <pre className="min-w-full px-4 py-3 font-mono text-[13px] leading-6">
          <code>
            {lines.map((line, i) => (
              <div key={i} className="flex">
                <span className="mr-4 inline-block w-8 flex-shrink-0 select-none text-right text-slate-600">
                  {i + 1}
                </span>
                <span className="whitespace-pre">{highlightLine(line)}</span>
              </div>
            ))}
          </code>
        </pre>
      </div>
    </div>
  );
}
