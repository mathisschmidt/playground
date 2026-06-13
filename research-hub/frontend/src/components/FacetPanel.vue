<script setup>
import { ref } from 'vue'
import { formatCount } from '../lib/dataset'

defineProps({
  column: { type: Object, required: true },
  counts: { type: Array, required: true }, // [{ value, count }] under current filters
  selected: { type: Set, required: true },
})
const emit = defineEmits(['toggle'])

const expanded = ref(false)
const VISIBLE = 8
</script>

<template>
  <section>
    <h3 class="mb-2 text-xs font-semibold uppercase tracking-wider text-slate-400">
      {{ column.name }}
    </h3>
    <ul class="space-y-0.5">
      <li
        v-for="item in expanded ? counts : counts.slice(0, VISIBLE)"
        :key="item.value"
      >
        <button
          class="flex w-full items-center gap-2 rounded-lg px-2 py-1.5 text-left text-xs transition hover:bg-white/5"
          :class="selected.has(item.value) ? 'bg-sky-400/10 text-sky-300' : 'text-slate-300'"
          @click="emit('toggle', column.name, item.value)"
        >
          <span
            class="grid h-3.5 w-3.5 shrink-0 place-items-center rounded border text-[9px]"
            :class="selected.has(item.value)
              ? 'border-sky-400 bg-sky-400 text-slate-950'
              : 'border-slate-600'"
          >
            <svg v-if="selected.has(item.value)" viewBox="0 0 10 10" class="h-2.5 w-2.5 fill-none stroke-current stroke-2">
              <path d="M1.5 5.5 4 8 8.5 2.5" />
            </svg>
          </span>
          <span class="flex-1 truncate">{{ item.value }}</span>
          <span class="font-mono text-[10px] text-slate-500">{{ formatCount(item.count) }}</span>
        </button>
      </li>
    </ul>
    <button
      v-if="counts.length > VISIBLE"
      class="mt-1 px-2 text-[11px] font-medium text-sky-400 hover:text-sky-300"
      @click="expanded = !expanded"
    >
      {{ expanded ? 'Show less' : `Show all ${counts.length}` }}
    </button>
  </section>
</template>
