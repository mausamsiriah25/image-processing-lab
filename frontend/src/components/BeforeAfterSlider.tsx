import { useRef, useState } from "react";

interface Props {
  beforeSrc: string;
  afterSrc: string;
  beforeLabel?: string;
  afterLabel?: string;
}

export default function BeforeAfterSlider({
  beforeSrc,
  afterSrc,
  beforeLabel = "Original",
  afterLabel = "Processed",
}: Props) {
  const [position, setPosition] = useState(50);
  const containerRef = useRef<HTMLDivElement>(null);

  const updateFromClientX = (clientX: number) => {
    const el = containerRef.current;
    if (!el) return;
    const rect = el.getBoundingClientRect();
    const pct = ((clientX - rect.left) / rect.width) * 100;
    setPosition(Math.min(100, Math.max(0, pct)));
  };

  return (
    <div
      ref={containerRef}
      className="relative aspect-video w-full select-none overflow-hidden rounded-xl border border-slate-200 bg-slate-100 dark:border-white/10 dark:bg-black/30"
      onMouseMove={(e) => {
        if (e.buttons === 1) updateFromClientX(e.clientX);
      }}
      onTouchMove={(e) => updateFromClientX(e.touches[0].clientX)}
    >
      <img src={afterSrc} alt={afterLabel} className="absolute inset-0 h-full w-full object-contain" />
      <div className="absolute inset-0 overflow-hidden" style={{ width: `${position}%` }}>
        <img src={beforeSrc} alt={beforeLabel} className="h-full w-full object-contain" style={{ width: containerRef.current?.clientWidth }} />
      </div>

      <div
        className="absolute inset-y-0 flex w-0.5 -translate-x-1/2 cursor-ew-resize items-center bg-white/90"
        style={{ left: `${position}%` }}
        role="slider"
        aria-label="Before/after comparison position"
        aria-valuenow={Math.round(position)}
        aria-valuemin={0}
        aria-valuemax={100}
        tabIndex={0}
        onKeyDown={(e) => {
          if (e.key === "ArrowLeft") setPosition((p) => Math.max(0, p - 5));
          if (e.key === "ArrowRight") setPosition((p) => Math.min(100, p + 5));
        }}
      >
        <span className="flex h-7 w-7 -translate-x-1/2 items-center justify-center rounded-full bg-white shadow">
          <span className="h-2 w-2 rounded-full bg-brand-600" />
        </span>
      </div>

      <span className="absolute left-2 top-2 rounded bg-black/60 px-2 py-0.5 text-xs text-white">{beforeLabel}</span>
      <span className="absolute right-2 top-2 rounded bg-black/60 px-2 py-0.5 text-xs text-white">{afterLabel}</span>
    </div>
  );
}
