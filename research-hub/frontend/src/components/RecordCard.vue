<script setup>
import Chip from './Chip.vue'
import { asHref } from '../lib/dataset'

const props = defineProps({
  row: { type: Array, required: true },
  roles: { type: Object, required: true },
})

const v = (col) => (col ? props.row[col.i] : '')
</script>

<template>
  <article
    class="group flex flex-col rounded-2xl border border-white/10 bg-slate-900/60 p-5 transition hover:border-sky-400/30 hover:bg-slate-900 hover:shadow-lg hover:shadow-sky-500/5"
  >
    <div class="flex items-start justify-between gap-3">
      <div class="min-w-0">
        <h3 class="truncate text-base font-semibold text-white" :title="v(roles.title)">
          {{ v(roles.title) || '—' }}
        </h3>
        <p v-if="v(roles.subtitle)" class="mt-0.5 flex items-center gap-1 text-xs text-slate-400">
          <svg viewBox="0 0 20 20" class="h-3 w-3 fill-current opacity-60">
            <path fill-rule="evenodd" d="M9.69 18.933l.003.001a.75.75 0 00.614 0l.003-.001.018-.008a5.741 5.741 0 00.281-.14c.186-.096.446-.24.757-.433.62-.384 1.445-.966 2.274-1.765C15.302 14.988 17 12.493 17 9.5 17 5.358 13.866 2 10 2S3 5.358 3 9.5c0 2.993 1.698 5.488 3.355 7.087a15.1 15.1 0 002.273 1.765 11.842 11.842 0 001.062.607zM10 11.25a2.25 2.25 0 100-4.5 2.25 2.25 0 000 4.5z" clip-rule="evenodd" />
          </svg>
          {{ v(roles.subtitle) }}
        </p>
      </div>
      <div
        v-for="m in roles.metrics"
        :key="m.name"
        v-show="v(m)"
        class="shrink-0 rounded-lg bg-white/5 px-2 py-1 text-center ring-1 ring-white/10"
      >
        <p class="text-[9px] uppercase tracking-wider text-slate-500">{{ m.name }}</p>
        <p class="font-mono text-xs font-semibold text-slate-200">{{ v(m) }}</p>
      </div>
    </div>

    <div v-if="roles.facets.some((f) => v(f))" class="mt-3 flex flex-wrap gap-1.5">
      <template v-for="f in roles.facets" :key="f.name">
        <Chip v-if="v(f)" :value="v(f)" />
      </template>
    </div>

    <p v-if="v(roles.description)" class="mt-3 line-clamp-4 text-[13px] leading-relaxed text-slate-400">
      {{ v(roles.description) }}
    </p>

    <dl v-if="roles.details.some((d) => v(d))" class="mt-3 space-y-1">
      <div v-for="d in roles.details" :key="d.name" v-show="v(d)" class="flex gap-2 text-xs">
        <dt class="shrink-0 text-slate-500">{{ d.name }}:</dt>
        <dd class="truncate text-slate-300" :title="v(d)">{{ v(d) }}</dd>
      </div>
    </dl>

    <div v-if="roles.links.some((l) => v(l))" class="mt-auto pt-4">
      <a
        v-for="l in roles.links"
        :key="l.name"
        v-show="v(l)"
        :href="asHref(v(l))"
        target="_blank"
        rel="noopener noreferrer"
        class="inline-flex items-center gap-1.5 text-xs font-medium text-sky-400 hover:text-sky-300"
        @click.stop
      >
        <svg viewBox="0 0 20 20" class="h-3.5 w-3.5 fill-current">
          <path d="M12.232 4.232a2.5 2.5 0 013.536 3.536l-1.225 1.224a.75.75 0 001.061 1.06l1.224-1.224a4 4 0 00-5.656-5.656l-3 3a4 4 0 00.225 5.865.75.75 0 00.977-1.138 2.5 2.5 0 01-.142-3.667l3-3z" />
          <path d="M11.603 7.963a.75.75 0 00-.977 1.138 2.5 2.5 0 01.142 3.667l-3 3a2.5 2.5 0 01-3.536-3.536l1.225-1.224a.75.75 0 00-1.061-1.06l-1.224 1.224a4 4 0 105.656 5.656l3-3a4 4 0 00-.225-5.865z" />
        </svg>
        {{ v(l) }}
      </a>
    </div>
  </article>
</template>
