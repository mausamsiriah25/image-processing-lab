import { Link } from "react-router-dom";
import {
  ArrowRight,
  Code2,
  Download,
  ImageIcon,
  LineChart,
  SlidersHorizontal,
  Sparkles,
} from "lucide-react";
import { usePracticalList } from "../hooks/usePracticals";

const FEATURES = [
  {
    icon: Sparkles,
    title: "Interactive Experiments",
    body: "Run every practical live in your browser — no local Python setup required.",
  },
  {
    icon: ImageIcon,
    title: "Real Image Processing",
    body: "Every experiment calls the actual OpenCV/NumPy backend. Nothing is simulated.",
  },
  {
    icon: Code2,
    title: "Python Implementations",
    body: "Read the exact reference code taught in class, with syntax highlighting and copy support.",
  },
  {
    icon: LineChart,
    title: "Visual Results",
    body: "See histograms, comparison grids, and numeric analysis alongside your processed images.",
  },
  {
    icon: SlidersHorizontal,
    title: "Parameter Controls",
    body: "Tune thresholds, kernels, and other parameters and immediately see the effect.",
  },
  {
    icon: Download,
    title: "PDF Reports",
    body: "Generate a properly formatted practical report with one click.",
  },
];

const STEPS = [
  { n: 1, title: "Choose a Practical", body: "Browse the dashboard and pick a topic." },
  { n: 2, title: "Learn the Theory", body: "Read the Aim, Objectives, Theory and Algorithm." },
  { n: 3, title: "Upload an Image", body: "Bring your own image (where the practical needs one)." },
  { n: 4, title: "Run the Experiment", body: "The backend runs the real algorithm on your image." },
  { n: 5, title: "Analyze the Result", body: "Compare outputs, histograms, and numeric results." },
  { n: 6, title: "Generate a Report", body: "Download a formatted PDF of your practical." },
];

export default function HomePage() {
  const { data: practicals } = usePracticalList();
  const total = practicals?.length ?? 11;

  return (
    <div>
      {/* Hero */}
      <section className="relative overflow-hidden bg-grid-pattern">
        <div className="absolute inset-0 bg-gradient-to-b from-brand-500/10 via-transparent to-transparent" />
        <div className="relative mx-auto max-w-5xl px-4 py-24 text-center sm:px-6 lg:px-8">
          <span className="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white/70 px-3 py-1 text-xs font-medium text-slate-600 dark:border-white/10 dark:bg-white/5 dark:text-slate-300">
            <Sparkles className="h-3.5 w-3.5 text-accent-500" /> A modern scientific-computing platform
          </span>
          <h1 className="mt-6 text-4xl font-bold tracking-tight sm:text-6xl">
            Image Processing <span className="text-brand-600 dark:text-accent-400">Lab</span>
          </h1>
          <p className="mx-auto mt-4 max-w-2xl text-lg text-slate-600 dark:text-slate-300">
            Learn. Experiment. Visualize.
          </p>
          <p className="mx-auto mt-3 max-w-2xl text-sm text-slate-500 dark:text-slate-400">
            An interactive laboratory covering image fundamentals, geometric transformations,
            enhancement, filtering, restoration, compression, morphology, and object detection —
            with real Python/OpenCV execution behind every experiment.
          </p>
          <div className="mt-8 flex flex-wrap items-center justify-center gap-3">
            <Link
              to="/practicals"
              className="inline-flex items-center gap-2 rounded-lg bg-brand-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-brand-700"
            >
              Explore Practicals <ArrowRight className="h-4 w-4" />
            </Link>
            <a
              href="#how-it-works"
              className="inline-flex items-center gap-2 rounded-lg border border-slate-300 px-5 py-3 text-sm font-semibold text-slate-700 transition hover:border-brand-400 dark:border-white/15 dark:text-slate-200"
            >
              How It Works
            </a>
          </div>
        </div>
      </section>

      {/* Stats */}
      <section className="border-y border-slate-200 bg-white/60 dark:border-white/10 dark:bg-white/5">
        <div className="mx-auto grid max-w-5xl grid-cols-3 gap-4 px-4 py-8 text-center sm:px-6 lg:px-8">
          <div>
            <p className="text-3xl font-bold text-brand-600 dark:text-accent-400">{total}</p>
            <p className="text-xs text-slate-500 dark:text-slate-400">Total Practicals</p>
          </div>
          <div>
            <p className="text-3xl font-bold text-brand-600 dark:text-accent-400">9+</p>
            <p className="text-xs text-slate-500 dark:text-slate-400">Image Processing Techniques</p>
          </div>
          <div>
            <p className="text-3xl font-bold text-brand-600 dark:text-accent-400">100%</p>
            <p className="text-xs text-slate-500 dark:text-slate-400">Real Backend Execution</p>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="mx-auto max-w-6xl px-4 py-20 sm:px-6 lg:px-8">
        <h2 className="text-center text-2xl font-bold sm:text-3xl">Everything a lab needs</h2>
        <div className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {FEATURES.map((f) => (
            <div
              key={f.title}
              className="rounded-xl border border-slate-200 bg-white p-6 transition hover:border-brand-300 hover:shadow-sm dark:border-white/10 dark:bg-white/5"
            >
              <f.icon className="h-6 w-6 text-brand-600 dark:text-accent-400" />
              <h3 className="mt-3 font-semibold">{f.title}</h3>
              <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">{f.body}</p>
            </div>
          ))}
        </div>
      </section>

      {/* How it works */}
      <section id="how-it-works" className="border-t border-slate-200 bg-white/60 py-20 dark:border-white/10 dark:bg-white/5">
        <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
          <h2 className="text-center text-2xl font-bold sm:text-3xl">How the Lab Works</h2>
          <div className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {STEPS.map((s) => (
              <div key={s.n} className="rounded-xl border border-slate-200 bg-base-50 p-5 dark:border-white/10 dark:bg-base-950">
                <span className="inline-flex h-8 w-8 items-center justify-center rounded-full bg-brand-600 text-sm font-bold text-white">
                  {s.n}
                </span>
                <h3 className="mt-3 font-semibold">{s.title}</h3>
                <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">{s.body}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="mx-auto max-w-4xl px-4 py-20 text-center sm:px-6 lg:px-8">
        <h2 className="text-2xl font-bold sm:text-3xl">Ready to start experimenting?</h2>
        <p className="mx-auto mt-3 max-w-xl text-slate-500 dark:text-slate-400">
          Jump into the dashboard and run your first real image-processing experiment.
        </p>
        <Link
          to="/practicals"
          className="mt-6 inline-flex items-center gap-2 rounded-lg bg-brand-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-brand-700"
        >
          Explore the Lab <ArrowRight className="h-4 w-4" />
        </Link>
      </section>
    </div>
  );
}
