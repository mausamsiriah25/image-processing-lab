import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { ArrowRight, Search } from "lucide-react";
import { usePracticalList } from "../hooks/usePracticals";

export default function PracticalsDashboard() {
  const { data: practicals, loading, error } = usePracticalList();
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState<string>("all");

  const categories = useMemo(() => {
    if (!practicals) return [];
    return Array.from(new Set(practicals.map((p) => p.category)));
  }, [practicals]);

  const filtered = useMemo(() => {
    if (!practicals) return [];
    return practicals.filter((p) => {
      const matchesQuery =
        query.trim() === "" ||
        p.title.toLowerCase().includes(query.toLowerCase()) ||
        p.aim.toLowerCase().includes(query.toLowerCase());
      const matchesCategory = category === "all" || p.category === category;
      return matchesQuery && matchesCategory;
    });
  }, [practicals, query, category]);

  return (
    <div className="mx-auto max-w-6xl px-4 py-12 sm:px-6 lg:px-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Practicals</h1>
        <p className="mt-2 text-slate-500 dark:text-slate-400">
          Browse every practical in the course and open one to read the theory, view the code,
          and run the experiment.
        </p>
      </div>

      <div className="mb-8 flex flex-col gap-3 sm:flex-row">
        <div className="relative flex-1">
          <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search practicals..."
            aria-label="Search practicals"
            className="w-full rounded-lg border border-slate-300 bg-white py-2.5 pl-9 pr-3 text-sm dark:border-white/15 dark:bg-white/5"
          />
        </div>
        <select
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          aria-label="Filter by category"
          className="rounded-lg border border-slate-300 bg-white px-3 py-2.5 text-sm dark:border-white/15 dark:bg-white/5"
        >
          <option value="all">All categories</option>
          {categories.map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </select>
      </div>

      {loading && (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3" aria-busy="true">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="h-40 animate-pulse rounded-xl border border-slate-200 bg-slate-100 dark:border-white/10 dark:bg-white/5" />
          ))}
        </div>
      )}

      {error && (
        <div role="alert" className="rounded-xl border border-rose-200 bg-rose-50 p-6 text-sm text-rose-700 dark:border-rose-900/40 dark:bg-rose-950/40 dark:text-rose-300">
          {error} — make sure the backend API is running and <code>VITE_API_URL</code> is configured correctly.
        </div>
      )}

      {!loading && !error && filtered.length === 0 && (
        <p className="text-sm text-slate-500 dark:text-slate-400">No practicals match your search.</p>
      )}

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {filtered.map((p) => (
          <Link
            key={p.id}
            to={`/practicals/${p.id}`}
            className="group flex flex-col rounded-xl border border-slate-200 bg-white p-5 transition hover:-translate-y-0.5 hover:border-brand-300 hover:shadow-md dark:border-white/10 dark:bg-white/5"
          >
            <div className="flex items-center justify-between">
              <span className="rounded-full bg-brand-50 px-2.5 py-1 text-xs font-semibold text-brand-700 dark:bg-brand-500/10 dark:text-accent-400">
                {p.type === "postlab" ? `Post Lab ${p.number}` : `Practical ${String(p.number).padStart(2, "0")}`}
              </span>
              <span className="text-xs text-slate-400">{p.category}</span>
            </div>
            <h3 className="mt-3 font-semibold group-hover:text-brand-600 dark:group-hover:text-accent-400">
              {p.title}
            </h3>
            <p className="mt-1 line-clamp-2 flex-1 text-sm text-slate-500 dark:text-slate-400">{p.aim}</p>
            <span className="mt-4 inline-flex items-center gap-1 text-sm font-medium text-brand-600 dark:text-accent-400">
              Open Practical <ArrowRight className="h-3.5 w-3.5 transition group-hover:translate-x-0.5" />
            </span>
          </Link>
        ))}
      </div>
    </div>
  );
}
