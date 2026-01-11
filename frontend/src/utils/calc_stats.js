export function formatSecondsToHM(seconds) {
  const s = Math.max(0, Number(seconds) || 0);
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  if (h > 0) return `${h}h ${m}min`;
  return `${m}min`;
}

export function formatPercentFromRatio(ratio) {
  const n = Number(ratio) || 0;
  return `${Math.round(n * 100)}%`;
}

export function calcPercentChange(current, previous) {
  const c = Number(current) || 0;
  const p = Number(previous) || 0;
  if (p <= 0) return null;
  return Math.round(((c - p) / p) * 100);
}
