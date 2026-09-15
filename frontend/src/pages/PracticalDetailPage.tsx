import { useEffect, useMemo, useState, type ReactNode } from "react";
import { Link, useParams } from "react-router-dom";
import {
  AlertTriangle,
  ChevronLeft,
  ChevronRight,
  FileText,
  Loader2,
  PlayCircle,
} from "lucide-react";

import { usePracticalDetail } from "../hooks/usePracticals";
import CodeViewer from "../components/CodeViewer";
import ImageUploader from "../components/ImageUploader";
import ParameterControls from "../components/ParameterControls";
import ResultGrid from "../components/ResultGrid";
import ReportDialog from "../components/ReportDialog";
import { runExperiment } from "../services/processingService";
import { ApiError } from "../services/api";
import type { ProcessingResult } from "../types/processing";
import { formatSeconds } from "../utils/format";

type Status = "idle" | "processing" | "success" | "error";

function fileToDataUrl(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result as string);
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

export default function PracticalDetailPage() {
  const { id } = useParams<{ id: string }>();
  const { data: practical, loading, error } = usePracticalDetail(id);

  const [image, setImage] = useState<File | null>(null);
  const [image2, setImage2] = useState<File | null>(null);
  const [template, setTemplate] = useState<File | null>(null);
  const [target, setTarget] = useState<File | null>(null);

  const [params, setParams] = useState<Record<string, string | number | boolean>>({});
  const [status, setStatus] = useState<Status>("idle");
  const [processingError, setProcessingError] = useState<string | null>(null);
  const [result, setResult] = useState<ProcessingResult | null>(null);
  const [reportOpen, setReportOpen] = useState(false);
  const [inputImageUrls, setInputImageUrls] = useState<Record<string, string>>({});

  useEffect(() => {
    if (!practical) return;
    const defaults: Record<string, string | number | boolean> = {};
    practical.parameters.forEach((p) => {
      defaults[p.key] = p.default;
    });
    setParams(defaults);
    setResult(null);
    setStatus("idle");
    setImage(null);
    setImage2(null);
    setTemplate(null);
    setTarget(null);
  }, [practical]);

  const needsSecondImage = practical?.id === "practical-02" && ["add", "addWeighted", "subtract", "bitwise_and", "bitwise_or", "bitwise_xor"].includes(String(params.operation));

  const canRun = useMemo(() => {
    if (!practical) return false;
    if (!practical.requiresImage) return true;
    if (practical.multiImage) return Boolean(template && target);
    if (needsSecondImage) return Boolean(image && image2);
    return Boolean(image);
  }, [practical, image, image2, template, target, needsSecondImage]);

  const handleParamChange = (key: string, value: string | number | boolean) => {
    setParams((prev) => ({ ...prev, [key]: value }));
  };

  const handleResetParams = () => {
    if (!practical) return;
    const defaults: Record<string, string | number | boolean> = {};
    practical.parameters.forEach((p) => {
      defaults[p.key] = p.default;
    });
    setParams(defaults);
  };

  const handleRun = async () => {
    if (!practical) return;
    setStatus("processing");
    setProcessingError(null);
    try {
      const res = await runExperiment(practical.id, { image, image2, template, target }, params);
      setResult(res);
      setStatus("success");

      const urls: Record<string, string> = {};
      if (image) urls.image = await fileToDataUrl(image);
      if (image2) urls.image2 = await fileToDataUrl(image2);
      if (template) urls.template = await fileToDataUrl(template);
      if (target) urls.target = await fileToDataUrl(target);
      setInputImageUrls(urls);
    } catch (err) {
      const message = err instanceof ApiError ? err.message : "Processing failed. Please try again.";
      setProcessingError(message);
      setStatus("error");
    }
  };

  if (loading) {
    return (
      <div className="mx-auto flex max-w-5xl items-center justify-center px-4 py-24">
        <Loader2 className="h-6 w-6 animate-spin text-brand-600" />
      </div>
    );
  }

  if (error || !practical) {
    return (
      <div className="mx-auto max-w-3xl px-4 py-20 text-center">
        <AlertTriangle className="mx-auto h-10 w-10 text-rose-500" />
        <p className="mt-4 text-slate-600 dark:text-slate-300">{error ?? "Practical not found."}</p>
        <Link to="/practicals" className="mt-4 inline-block text-brand-600 hover:underline dark:text-accent-400">
          Back to Practicals
        </Link>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-5xl px-4 py-10 sm:px-6 lg:px-8">
      <nav aria-label="Breadcrumb" className="mb-4 text-sm text-slate-500 dark:text-slate-400">
        <Link to="/practicals" className="hover:text-brand-600 dark:hover:text-accent-400">
          Practicals
        </Link>
        <span className="mx-2">/</span>
        <span className="text-slate-700 dark:text-slate-200">{practical.title}</span>
      </nav>

      <header className="mb-8">
        <span className="rounded-full bg-brand-50 px-2.5 py-1 text-xs font-semibold text-brand-700 dark:bg-brand-500/10 dark:text-accent-400">
          {practical.type === "postlab" ? `Post Lab ${practical.number}` : `Practical ${String(practical.number).padStart(2, "0")}`}
        </span>
        <h1 className="mt-3 text-3xl font-bold">{practical.title}</h1>
        <p className="mt-1 text-sm text-slate-400">{practical.category}</p>
      </header>

      <Section title="Aim">
        <p className="text-slate-600 dark:text-slate-300">{practical.aim}</p>
      </Section>

      {practical.objectives.length > 0 && (
        <Section title="Objectives">
          <ul className="list-disc space-y-1 pl-5 text-slate-600 dark:text-slate-300">
            {practical.objectives.map((o, i) => (
              <li key={i}>{o}</li>
            ))}
          </ul>
        </Section>
      )}

      <Section title="Theory">
        <p className="whitespace-pre-line text-slate-600 dark:text-slate-300">{practical.theory}</p>
      </Section>

      {practical.algorithm.length > 0 && (
        <Section title="Algorithm">
          <ol className="list-decimal space-y-1 pl-5 text-slate-600 dark:text-slate-300">
            {practical.algorithm.map((step, i) => (
              <li key={i}>{step}</li>
            ))}
          </ol>
        </Section>
      )}

      <Section title="Python Implementation (Reference)">
        <CodeViewer code={practical.referenceCode} />
        <p className="mt-3 text-xs text-slate-400">
          This is the original classroom implementation. Where it uses desktop-only calls (e.g.{" "}
          <code>cv2.imshow</code>) or local file paths, the lab runs an equivalent
          server-compatible implementation behind the scenes when you click "Run Experiment"
          below.
        </p>
      </Section>

      {/* Interactive Workspace */}
      <Section title="Interactive Experiment">
        <div className="space-y-5 rounded-2xl border border-slate-200 bg-white p-6 dark:border-white/10 dark:bg-white/5">
          {practical.requiresImage ? (
            practical.multiImage ? (
              <div className="grid gap-4 sm:grid-cols-2">
                <ImageUploader label="Template Image" file={template} onChange={setTemplate} required />
                <ImageUploader label="Target Image" file={target} onChange={setTarget} required />
              </div>
            ) : (
              <div className={`grid gap-4 ${needsSecondImage ? "sm:grid-cols-2" : ""}`}>
                <ImageUploader label="Input Image" file={image} onChange={setImage} required />
                {needsSecondImage && (
                  <ImageUploader label="Second Image" file={image2} onChange={setImage2} required />
                )}
              </div>
            )
          ) : (
            <p className="text-sm text-slate-500 dark:text-slate-400">
              This practical is a setup/prelab exercise and does not require an uploaded image.
            </p>
          )}

          <ParameterControls
            parameters={practical.parameters}
            values={params}
            onChange={handleParamChange}
            onReset={handleResetParams}
          />

          <button
            type="button"
            onClick={handleRun}
            disabled={!canRun || status === "processing"}
            className="inline-flex items-center gap-2 rounded-lg bg-brand-600 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-brand-700 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {status === "processing" ? <Loader2 className="h-4 w-4 animate-spin" /> : <PlayCircle className="h-4 w-4" />}
            {status === "processing" ? "Processing…" : "Run Experiment"}
          </button>

          {processingError && (
            <p role="alert" className="flex items-center gap-1.5 text-sm text-rose-600 dark:text-rose-400">
              <AlertTriangle className="h-4 w-4" /> {processingError}
            </p>
          )}
        </div>
      </Section>

      {result && (
        <Section title="Results">
          <p className="mb-4 text-sm text-slate-400">
            Processing Time: <span className="font-mono text-slate-600 dark:text-slate-300">{formatSeconds(result.processingTime)}</span>
          </p>
          {result.warnings.length > 0 && (
            <ul className="mb-4 space-y-1 text-sm text-amber-600 dark:text-amber-400">
              {result.warnings.map((w, i) => (
                <li key={i}>⚠ {w}</li>
              ))}
            </ul>
          )}
          <ResultGrid outputs={result.outputs} />

          <button
            type="button"
            onClick={() => setReportOpen(true)}
            className="mt-6 inline-flex items-center gap-2 rounded-lg border border-brand-300 px-5 py-2.5 text-sm font-semibold text-brand-700 transition hover:bg-brand-50 dark:border-accent-400/40 dark:text-accent-400 dark:hover:bg-accent-500/10"
          >
            <FileText className="h-4 w-4" /> Generate Report
          </button>
        </Section>
      )}

      <Section title="Observation">
        <p className="text-slate-600 dark:text-slate-300">{practical.observation}</p>
      </Section>

      <Section title="Conclusion">
        <p className="text-slate-600 dark:text-slate-300">{practical.conclusion}</p>
      </Section>

      {practical.postLab.length > 0 && (
        <Section title="Post-Lab">
          <ul className="list-disc space-y-1 pl-5 text-slate-600 dark:text-slate-300">
            {practical.postLab.map((q, i) => (
              <li key={i}>{q}</li>
            ))}
          </ul>
        </Section>
      )}

      <PracticalNavigation currentId={practical.id} />

      {result && (
        <ReportDialog
          open={reportOpen}
          onClose={() => setReportOpen(false)}
          practicalId={practical.id}
          result={result}
          inputImages={inputImageUrls}
        />
      )}
    </div>
  );
}

function Section({ title, children }: { title: string; children: ReactNode }) {
  return (
    <section className="mb-10">
      <h2 className="mb-3 text-xl font-semibold">{title}</h2>
      {children}
    </section>
  );
}

const ORDER = [
  "practical-01", "practical-02", "practical-03", "practical-04", "practical-05",
  "practical-06", "practical-07", "practical-08", "practical-09", "postlab-02", "postlab-03",
];

function PracticalNavigation({ currentId }: { currentId: string }) {
  const idx = ORDER.indexOf(currentId);
  const prev = idx > 0 ? ORDER[idx - 1] : null;
  const next = idx >= 0 && idx < ORDER.length - 1 ? ORDER[idx + 1] : null;

  return (
    <nav className="mt-10 flex items-center justify-between border-t border-slate-200 pt-6 dark:border-white/10" aria-label="Practical navigation">
      {prev ? (
        <Link to={`/practicals/${prev}`} className="inline-flex items-center gap-1 text-sm text-brand-600 hover:underline dark:text-accent-400">
          <ChevronLeft className="h-4 w-4" /> Previous
        </Link>
      ) : (
        <span />
      )}
      {next ? (
        <Link to={`/practicals/${next}`} className="inline-flex items-center gap-1 text-sm text-brand-600 hover:underline dark:text-accent-400">
          Next <ChevronRight className="h-4 w-4" />
        </Link>
      ) : (
        <span />
      )}
    </nav>
  );
}
