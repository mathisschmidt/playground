<script setup>
import { computed } from 'vue'
import { barClass, formatCount } from '../lib/dataset'

const props = defineProps({
  title: { type: String, required: true },
  items: { type: Array, required: true }, // [{ value, count }]
  limit: { type: Number, default: 12 },
})

const shown = computed(() => props.items.slice(0, props.limit))
const max = computed(() => Math.max(1, ...props.items.map((i) => i.count)))
const rest = computed(() =>
  props.items.slice(props.limit).reduce((s, i) => s + i.count, 0)
)
</script>

<template>
  <div class="rounded-2xl border border-white/10 bg-slate-900/60 p-5">
    <h3 class="mb-4 text-sm font-semibold uppercase tracking-wider text-slate-400">{{ title }}</h3>
    <div class="space-y-2.5">
      <div v-for="item in shown" :key="item.value" class="group">
        <div class="mb-1 flex items-baseline justify-between gap-3 text-xs">
          <span class="truncate text-slate-300">{{ item.value }}</span>
          <span class="font-mono text-slate-500">{{ formatCount(item.count) }}</span>
        </div>
        <div class="h-1.5 overflow-hidden rounded-full bg-white/5">
          <div
            class="h-full rounded-full opacity-80 transition-all group-hover:opacity-100"
            :class="barClass(item.value)"
            :style="{ width: (item.count / max) * 100 + '%' }"
          />
        </div>
      </div>
      <p v-if="rest > 0" class="pt-1 text-[11px] text-slate-500">
        + {{ formatCount(rest) }} in {{ items.length - limit }} more
      </p>
    </div>
  </div>
</template>
