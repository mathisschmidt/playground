<script setup>
import { onMounted, ref } from 'vue'
import { fetchDatasets } from '../api'
import { formatCount } from '../lib/dataset'

const datasets = ref([])
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    datasets.value = await fetchDatasets()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})

const fmtDate = (iso) =>
  new Date(iso).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })
</script>

<template>
  <div>
    <div class="mb-10">
      <h1 class="text-3xl font-bold tracking-tight text-white">Datasets</h1>
      <p class="mt-2 max-w-2xl text-sm text-slate-400">
        Every CSV dropped into <code class="rounded bg-white/5 px-1.5 py-0.5 text-sky-300">research-hub/data/</code>
        appears here, automatically profiled and rendered with a layout that fits its content.
      </p>
    </div>

    <div v-if="loading" class="text-sm text-slate-500">Loading datasets…</div>
    <div v-else-if="error" class="rounded-xl border border-rose-500/30 bg-rose-500/10 p-4 text-sm text-rose-300">
      Could not reach the API: {{ error }}. Is the backend running on port 8000?
    </div>

    <div v-else-if="datasets.length === 0" class="rounded-xl border border-dashed border-white/10 p-10 text-center text-sm text-slate-500">
      No datasets yet — drop a <code>.csv</code> file into <code>research-hub/data/</code> and refresh.
    </div>

    <div v-else class="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
      <RouterLink
        v-for="ds in datasets"
        :key="ds.slug"
        :to="{ name: 'dataset', params: { slug: ds.slug } }"
        class="group relative overflow-hidden rounded-2xl border border-white/10 bg-slate-900/60 p-6 transition hover:border-sky-400/40 hover:bg-slate-900"
      >
        <div class="absolute -right-10 -top-10 h-32 w-32 rounded-full bg-sky-500/10 blur-2xl transition group-hover:bg-sky-500/20" />
        <h2 class="text-lg font-semibold text-white group-hover:text-sky-300">{{ ds.title }}</h2>
        <p class="mt-1 text-xs text-slate-500">{{ ds.file }} · updated {{ fmtDate(ds.modified) }}</p>
        <p class="mt-4 text-3xl font-bold text-sky-400">
          {{ formatCount(ds.rowCount) }}
          <span class="text-sm font-medium text-slate-400">records</span>
        </p>
        <div class="mt-4 flex flex-wrap gap-1.5">
          <span
            v-for="col in ds.columns.slice(0, 6)"
            :key="col"
            class="rounded-md bg-white/5 px-2 py-0.5 text-[11px] text-slate-400 ring-1 ring-white/10"
          >{{ col }}</span>
          <span v-if="ds.columns.length > 6" class="px-1 text-[11px] text-slate-500">
            +{{ ds.columns.length - 6 }}
          </span>
        </div>
      </RouterLink>
    </div>
  </div>
</template>
