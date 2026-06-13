<script setup>
import { computed, ref, watch } from 'vue'
import { fetchDataset } from '../api'
import { pickRoles, formatCount } from '../lib/dataset'
import RecordCard from '../components/RecordCard.vue'
import DataTable from '../components/DataTable.vue'
import FacetPanel from '../components/FacetPanel.vue'
import BarChart from '../components/BarChart.vue'

const props = defineProps({ slug: { type: String, required: true } })

const ds = ref(null)
const error = ref(null)
const search = ref('')
const filters = ref({}) // column name -> Set of selected values
const view = ref('cards')
const sortKey = ref(null)
const sortDir = ref(1)
const showFilters = ref(false)

watch(
  () => props.slug,
  async (slug) => {
    ds.value = null
    error.value = null
    search.value = ''
    filters.value = {}
    sortKey.value = null
    try {
      ds.value = await fetchDataset(slug)
    } catch (e) {
      error.value = e.message
    }
  },
  { immediate: true }
)

const roles = computed(() => (ds.value ? pickRoles(ds.value.columns) : null))

function toggleFacet(name, value) {
  const next = { ...filters.value }
  const set = new Set(next[name] ?? [])
  set.has(value) ? set.delete(value) : set.add(value)
  if (set.size) next[name] = set
  else delete next[name]
  filters.value = next
}

const activeFilterCount = computed(() =>
  Object.values(filters.value).reduce((s, set) => s + set.size, 0)
)

function clearAll() {
  filters.value = {}
  search.value = ''
}

function passes(row, { except = null } = {}) {
  const q = search.value.trim().toLowerCase()
  if (q && !row.some((cell) => cell.toLowerCase().includes(q))) return false
  for (const facet of roles.value.facets) {
    if (facet.name === except) continue
    const set = filters.value[facet.name]
    if (set && !set.has(row[facet.i])) return false
  }
  return true
}

const filteredRows = computed(() => {
  if (!ds.value) return []
  return ds.value.rows.filter((row) => passes(row))
})

// Facet counts respect every other active filter (classic faceted search).
const facetCounts = computed(() => {
  const out = {}
  if (!ds.value) return out
  for (const facet of roles.value.facets) {
    const counts = new Map()
    for (const row of ds.value.rows) {
      const v = row[facet.i]
      if (v && passes(row, { except: facet.name })) {
        counts.set(v, (counts.get(v) ?? 0) + 1)
      }
    }
    out[facet.name] = [...counts.entries()]
      .map(([value, count]) => ({ value, count }))
      .sort((a, b) => b.count - a.count || a.value.localeCompare(b.value))
  }
  return out
})

function setSort(i) {
  if (sortKey.value === i) {
    sortDir.value = -sortDir.value
  } else {
    sortKey.value = i
    sortDir.value = 1
  }
}

const sortedRows = computed(() => {
  const rows = filteredRows.value
  const i = sortKey.value
  if (i === null) return rows
  const col = roles.value.all[i]
  const numeric = col.type === 'number' || col.type === 'year'
  return [...rows].sort((a, b) => {
    const av = a[i]
    const bv = b[i]
    if (!av) return 1
    if (!bv) return -1
    const cmp = numeric ? parseFloat(av) - parseFloat(bv) : av.localeCompare(bv)
    return cmp * sortDir.value
  })
})

// Insights: distribution of each facet plus year timeline, over filtered rows.
const insightCharts = computed(() => {
  if (!ds.value) return []
  const charts = []
  for (const facet of roles.value.facets) {
    const counts = new Map()
    for (const row of filteredRows.value) {
      const v = row[facet.i]
      if (v) counts.set(v, (counts.get(v) ?? 0) + 1)
    }
    charts.push({
      title: `By ${facet.name}`,
      items: [...counts.entries()]
        .map(([value, count]) => ({ value, count }))
        .sort((a, b) => b.count - a.count),
    })
  }
  for (const metric of roles.value.metrics.filter((m) => m.type === 'year')) {
    const counts = new Map()
    for (const row of filteredRows.value) {
      const v = row[metric.i]
      if (v) counts.set(v, (counts.get(v) ?? 0) + 1)
    }
    charts.push({
      title: `By ${metric.name}`,
      items: [...counts.entries()]
        .map(([value, count]) => ({ value, count }))
        .sort((a, b) => a.value.localeCompare(b.value)),
      limit: 50,
    })
  }
  return charts
})

const kpis = computed(() => {
  if (!ds.value) return []
  const items = [
    {
      label: 'records',
      value:
        filteredRows.value.length === ds.value.rowCount
          ? formatCount(ds.value.rowCount)
          : `${formatCount(filteredRows.value.length)} / ${formatCount(ds.value.rowCount)}`,
    },
  ]
  for (const facet of roles.value.facets) {
    items.push({ label: facet.name.toLowerCase(), value: formatCount(facet.distinct) })
  }
  for (const metric of roles.value.metrics) {
    if (metric.min != null && metric.min !== metric.max) {
      const fmt = (n) => (metric.type === 'year' ? String(Math.trunc(n)) : formatCount(n))
      items.push({ label: metric.name.toLowerCase(), value: `${fmt(metric.min)}–${fmt(metric.max)}` })
    }
  }
  return items.slice(0, 5)
})

const VIEWS = [
  { id: 'cards', label: 'Cards' },
  { id: 'table', label: 'Table' },
  { id: 'insights', label: 'Insights' },
]
</script>

<template>
  <div v-if="error" class="rounded-xl border border-rose-500/30 bg-rose-500/10 p-4 text-sm text-rose-300">
    {{ error }}
  </div>
  <div v-else-if="!ds" class="text-sm text-slate-500">Loading dataset…</div>

  <div v-else>
    <nav class="mb-4 text-xs text-slate-500">
      <RouterLink to="/" class="hover:text-sky-400">Datasets</RouterLink>
      <span class="mx-1.5">/</span>
      <span class="text-slate-300">{{ ds.title }}</span>
    </nav>

    <div class="mb-6 flex flex-wrap items-end justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold tracking-tight text-white">{{ ds.title }}</h1>
        <p class="mt-1 text-xs text-slate-500">{{ ds.file }}</p>
      </div>
      <div class="flex flex-wrap gap-2">
        <div
          v-for="kpi in kpis"
          :key="kpi.label"
          class="rounded-xl border border-white/10 bg-slate-900/60 px-3.5 py-2"
        >
          <p class="text-sm font-bold text-sky-400">{{ kpi.value }}</p>
          <p class="text-[10px] uppercase tracking-wider text-slate-500">{{ kpi.label }}</p>
        </div>
      </div>
    </div>

    <div class="mb-6 flex flex-wrap items-center gap-3">
      <div class="relative min-w-56 flex-1">
        <svg viewBox="0 0 20 20" class="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 fill-slate-500">
          <path fill-rule="evenodd" d="M9 3.5a5.5 5.5 0 100 11 5.5 5.5 0 000-11zM2 9a7 7 0 1112.452 4.391l3.328 3.329a.75.75 0 11-1.06 1.06l-3.329-3.328A7 7 0 012 9z" clip-rule="evenodd" />
        </svg>
        <input
          v-model="search"
          type="search"
          placeholder="Search all fields…"
          class="w-full rounded-xl border border-white/10 bg-slate-900/60 py-2 pl-10 pr-4 text-sm text-slate-200 placeholder:text-slate-500 focus:border-sky-400/50 focus:outline-none"
        />
      </div>

      <div class="flex rounded-xl border border-white/10 bg-slate-900/60 p-1">
        <button
          v-for="v in VIEWS"
          :key="v.id"
          class="rounded-lg px-3 py-1.5 text-xs font-medium transition"
          :class="view === v.id ? 'bg-sky-400/15 text-sky-300' : 'text-slate-400 hover:text-slate-200'"
          @click="view = v.id"
        >{{ v.label }}</button>
      </div>

      <button
        v-if="roles.facets.length"
        class="rounded-xl border border-white/10 bg-slate-900/60 px-3 py-2 text-xs font-medium text-slate-300 lg:hidden"
        @click="showFilters = !showFilters"
      >
        Filters
        <span v-if="activeFilterCount" class="ml-1 rounded-full bg-sky-400/20 px-1.5 text-sky-300">{{ activeFilterCount }}</span>
      </button>

      <button
        v-if="activeFilterCount || search"
        class="text-xs font-medium text-rose-400 hover:text-rose-300"
        @click="clearAll"
      >
        Clear all
      </button>
    </div>

    <div class="flex flex-col gap-8 lg:flex-row">
      <aside
        v-if="roles.facets.length"
        class="w-full shrink-0 space-y-6 lg:block lg:w-60"
        :class="showFilters ? 'block' : 'hidden'"
      >
        <FacetPanel
          v-for="facet in roles.facets"
          :key="facet.name"
          :column="facet"
          :counts="facetCounts[facet.name] ?? []"
          :selected="filters[facet.name] ?? new Set()"
          @toggle="toggleFacet"
        />
      </aside>

      <div class="min-w-0 flex-1">
        <p v-if="!filteredRows.length" class="rounded-xl border border-dashed border-white/10 p-10 text-center text-sm text-slate-500">
          No records match the current filters.
        </p>

        <div v-else-if="view === 'cards'" class="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
          <RecordCard v-for="(row, i) in sortedRows" :key="i" :row="row" :roles="roles" />
        </div>

        <DataTable
          v-else-if="view === 'table'"
          :columns="roles.all"
          :rows="sortedRows"
          :sort-key="sortKey"
          :sort-dir="sortDir"
          @sort="setSort"
        />

        <div v-else class="grid gap-5 md:grid-cols-2">
          <BarChart
            v-for="chart in insightCharts"
            :key="chart.title"
            :title="chart.title"
            :items="chart.items"
            :limit="chart.limit ?? 12"
          />
        </div>
      </div>
    </div>
  </div>
</template>
