import { useState } from "react";
import { Link, NavLink } from "react-router-dom";
import { Menu, X, FlaskConical } from "lucide-react";
import ThemeToggle from "./ThemeToggle";

interface Props {
  theme: "dark" | "light";
  onToggleTheme: () => void;
}

const links = [
  { to: "/", label: "Home" },
  { to: "/practicals", label: "Practicals" },
  { to: "/about", label: "About" },
];

export default function Navbar({ theme, onToggleTheme }: Props) {
  const [open, setOpen] = useState(false);

  return (
    <header className="sticky top-0 z-40 border-b border-slate-200/70 bg-base-50/80 backdrop-blur-md dark:border-white/10 dark:bg-base-950/80">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6 lg:px-8">
        <Link to="/" className="flex items-center gap-2 font-semibold tracking-tight">
          <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-brand-500 to-accent-500 text-white">
            <FlaskConical className="h-4 w-4" />
          </span>
          <span className="text-base">
            Image Processing <span className="text-brand-500">Lab</span>
          </span>
        </Link>

        <nav className="hidden items-center gap-8 md:flex" aria-label="Primary">
          {links.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) =>
                `text-sm font-medium transition ${
                  isActive
                    ? "text-brand-600 dark:text-accent-400"
                    : "text-slate-600 hover:text-brand-600 dark:text-slate-300 dark:hover:text-accent-400"
                }`
              }
            >
              {link.label}
            </NavLink>
          ))}
        </nav>

        <div className="flex items-center gap-2">
          <ThemeToggle theme={theme} onToggle={onToggleTheme} />
          <Link
            to="/practicals"
            className="hidden rounded-lg bg-brand-600 px-4 py-2 text-sm font-semibold text-white transition hover:bg-brand-700 sm:inline-flex"
          >
            Explore Lab
          </Link>
          <button
            type="button"
            className="inline-flex h-9 w-9 items-center justify-center rounded-lg border border-slate-200 dark:border-white/10 md:hidden"
            aria-label="Toggle navigation menu"
            aria-expanded={open}
            onClick={() => setOpen((v) => !v)}
          >
            {open ? <X className="h-4 w-4" /> : <Menu className="h-4 w-4" />}
          </button>
        </div>
      </div>

      {open && (
        <nav className="border-t border-slate-200 px-4 py-3 dark:border-white/10 md:hidden" aria-label="Mobile">
          <ul className="flex flex-col gap-3">
            {links.map((link) => (
              <li key={link.to}>
                <NavLink
                  to={link.to}
                  onClick={() => setOpen(false)}
                  className="block text-sm font-medium text-slate-700 dark:text-slate-200"
                >
                  {link.label}
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>
      )}
    </header>
  );
}
