import { Link } from "react-router-dom";

export default function Footer() {
  return (
    <footer className="border-t border-slate-200 bg-base-50 dark:border-white/10 dark:bg-base-950">
      <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
        <div className="grid gap-8 md:grid-cols-3">
          <div>
            <p className="font-semibold">Image Processing Lab</p>
            <p className="mt-2 max-w-xs text-sm text-slate-500 dark:text-slate-400">
              An interactive laboratory for learning and running real image-processing
              experiments with Python and OpenCV.
            </p>
          </div>
          <div>
            <p className="text-sm font-semibold text-slate-700 dark:text-slate-200">Explore</p>
            <ul className="mt-3 space-y-2 text-sm text-slate-500 dark:text-slate-400">
              <li>
                <Link to="/practicals" className="hover:text-brand-600 dark:hover:text-accent-400">
                  All Practicals
                </Link>
              </li>
              <li>
                <Link to="/about" className="hover:text-brand-600 dark:hover:text-accent-400">
                  About the Lab
                </Link>
              </li>
            </ul>
          </div>
          <div>
            <p className="text-sm font-semibold text-slate-700 dark:text-slate-200">Course</p>
            <p className="mt-3 text-sm text-slate-500 dark:text-slate-400">
              Image Processing Lab — Course Code N-PECCS502P
            </p>
          </div>
        </div>
        <p className="mt-8 border-t border-slate-200 pt-6 text-xs text-slate-400 dark:border-white/10">
          Built for current and future students of the Image Processing course.
        </p>
      </div>
    </footer>
  );
}
