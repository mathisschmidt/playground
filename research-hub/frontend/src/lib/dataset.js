// Helpers shared by the dataset views. Columns come from the backend
// profiler with a `type` and `role`; here we add the row index and a
// deterministic chip colour per value.

export function indexColumns(columns) {
  return columns.map((c, i) => ({ ...c, i }))
}

export function pickRoles(columns) {
  const cols = indexColumns(columns)
  return {
    title: cols.find((c) => c.role === 'title') ?? cols[0],
    subtitle: cols.find((c) => c.role === 'subtitle'),
    description: cols.find((c) => c.role === 'description'),
    links: cols.filter((c) => c.role === 'link'),
    facets: cols.filter((c) => c.role === 'facet'),
    metrics: cols.filter((c) => c.role === 'metric'),
    details: cols.filter((c) => c.role === 'detail'),
    all: cols,
  }
}

const PALETTE = [
  'bg-sky-400/10 text-sky-300 ring-sky-400/30',
  'bg-violet-400/10 text-violet-300 ring-violet-400/30',
  'bg-emerald-400/10 text-emerald-300 ring-emerald-400/30',
  'bg-amber-400/10 text-amber-300 ring-amber-400/30',
  'bg-rose-400/10 text-rose-300 ring-rose-400/30',
  'bg-cyan-400/10 text-cyan-300 ring-cyan-400/30',
  'bg-lime-400/10 text-lime-300 ring-lime-400/30',
  'bg-fuchsia-400/10 text-fuchsia-300 ring-fuchsia-400/30',
  'bg-orange-400/10 text-orange-300 ring-orange-400/30',
  'bg-indigo-400/10 text-indigo-300 ring-indigo-400/30',
]

const BAR_PALETTE = [
  'bg-sky-400',
  'bg-violet-400',
  'bg-emerald-400',
  'bg-amber-400',
  'bg-rose-400',
  'bg-cyan-400',
  'bg-lime-400',
  'bg-fuchsia-400',
  'bg-orange-400',
  'bg-indigo-400',
]

function hash(str) {
  let h = 0
  for (let i = 0; i < str.length; i++) h = (h * 31 + str.charCodeAt(i)) | 0
  return Math.abs(h)
}

export const chipClass = (value) => PALETTE[hash(value) % PALETTE.length]
export const barClass = (value) => BAR_PALETTE[hash(value) % BAR_PALETTE.length]

export function asHref(value) {
  return /^https?:\/\//i.test(value) ? value : `https://${value}`
}

export function formatCount(n) {
  return new Intl.NumberFormat('en-US').format(n)
}
