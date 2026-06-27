<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { fetchDatasets, uploadDataset } from '../api'
import { formatCount } from '../lib/dataset'

const router = useRouter()
const datasets = ref([])
const loading = ref(true)
const error = ref(null)

const fileInput = ref(null)
const uploading = ref(false)
const uploadError = ref(null)
const dragOver = ref(false)

async function load() {
  try {
    datasets.value = await fetchDatasets()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

onMounted(load)

function pickFile() {
  uploadError.value = null
  fileInput.value?.click()
}

async function handleFiles(files) {
  const file = files?.[0]
  if (!file) return
  if (!file.name.toLowerCase().endsWith('.csv')) {
    uploadError.value = 'Please choose a .csv file.'
    return
  }
  uploading.value = true
  uploadError.value = null
  try {
    const ds = await uploadDataset(file)
    await load()
    router.push({ name: 'dataset', params: { slug: ds.slug } })
  } catch (e) {
    uploadError.value = e.message
  } finally {
    uploading.value = false
    if (fileInput.value) fileInput.value.value = ''
  }
}

function onInputChange(e) {
  handleFiles(e.target.files)
}

function onDrop(e) {
  dragOver.value = false
  handleFiles(e.dataTransfer.files)
}

const fmtDate = (iso) =>
  new Date(iso).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })
</script>

<template>
  <div
    @dragover.prevent="dragOver = true"
    @dragleave.prevent="dragOver = false"
    @drop.prevent="onDrop"
  >
    <input ref="fileInput" type="file" accept=".csv,text/csv" class="hidden" @change="onInputChange" />

    <div class="mb-10 flex flex-wrap items-start justify-between gap-4">
      <div>
        <h1 class="text-3xl font-bold tracking-tight text-white">Datasets</h1>
        <p class="mt-2 max-w-2xl text-sm text-slate-400">
          Upload a CSV or drop one anywhere on this page — it's automatically profiled
          and rendered with a layout that fits its content.
        </p>
      </div>
      <button
        :disabled="uploading"
        class="inline-flex items-center gap-2 rounded-xl bg-gradient-to-br from-sky-400 to-indigo-600 px-4 py-2.5 text-sm font-semibold text-white shadow-lg shadow-indigo-500/20 transition hover:brightness-110 disabled:opacity-60"
        @click="pickFile"
      >
        <svg v-if="!uploading" viewBox="0 0 20 20" class="h-4 w-4 fill-current">
          <path d="M10 3a.75.75 0 01.75.75v6.5h6.5a.75.75 0 010 1.5h-6.5v6.5a.75.75 0 01-1.5 0v-6.5h-6.5a.75.75 0 010-1.5h6.5v-6.5A.75.75 0 0110 3z" />
        </svg>
        <svg v-else viewBox="0 0 24 24" class="h-4 w-4 animate-spin fill-none stroke-current stroke-2">
          <circle cx="12" cy="12" r="9" class="opacity-25" />
          <path d="M21 12a9 9 0 00-9-9" class="opacity-90" />
        </svg>
        {{ uploading ? 'Uploading…' : 'Upload CSV' }}
      </button>
    </div>

    <div
      v-if="uploadError"
      class="mb-6 rounded-xl border border-rose-500/30 bg-rose-500/10 p-3 text-sm text-rose-300"
    >
      Upload failed: {{ uploadError }}
    </div>

    <div v-if="loading" class="text-sm text-slate-500">Loading datasets…</div>
    <div v-else-if="error" class="rounded-xl border border-rose-500/30 bg-rose-500/10 p-4 text-sm text-rose-300">
      Could not reach the API: {{ error }}. Is the backend running on port 8000?
    </div>

    <button
      v-else-if="datasets.length === 0"
      class="flex w-full flex-col items-center gap-2 rounded-2xl border-2 border-dashed border-white/15 p-12 text-center text-sm text-slate-400 transition hover:border-sky-400/50 hover:text-slate-200"
      @click="pickFile"
    >
      <svg viewBox="0 0 24 24" class="h-8 w-8 fill-none stroke-current stroke-[1.5] text-slate-500">
        <path d="M12 16V4m0 0L8 8m4-4 4 4" />
        <path d="M4 16v2a2 2 0 002 2h12a2 2 0 002-2v-2" />
      </svg>
      No datasets yet — click to upload a <code>.csv</code>, or drag one here.
    </button>

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

    <!-- Drag overlay -->
    <div
      v-if="dragOver"
      class="pointer-events-none fixed inset-0 z-50 flex items-center justify-center bg-slate-950/70 backdrop-blur-sm"
    >
      <div class="rounded-2xl border-2 border-dashed border-sky-400/60 bg-slate-900/80 px-12 py-10 text-center">
        <p class="text-lg font-semibold text-sky-300">Drop your CSV to add it</p>
      </div>
    </div>
  </div>
</template>
