<script setup>
import Chip from './Chip.vue'
import { asHref } from '../lib/dataset'

defineProps({
  columns: { type: Array, required: true }, // indexed columns
  rows: { type: Array, required: true },
  sortKey: { type: Number, default: null },
  sortDir: { type: Number, default: 1 },
})
const emit = defineEmits(['sort'])
</script>

<template>
  <div class="overflow-x-auto rounded-2xl border border-white/10 bg-slate-900/60">
    <table class="w-full min-w-max text-left text-xs">
      <thead>
        <tr class="border-b border-white/10">
          <th
            v-for="col in columns"
            :key="col.name"
            class="sticky top-0 cursor-pointer select-none whitespace-nowrap bg-slate-900 px-4 py-3 font-semibold uppercase tracking-wider text-slate-400 hover:text-sky-300"
            @click="emit('sort', col.i)"
          >
            {{ col.name }}
            <span v-if="sortKey === col.i" class="ml-1 text-sky-400">{{ sortDir > 0 ? '▲' : '▼' }}</span>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(row, ri) in rows"
          :key="ri"
          class="border-b border-white/5 transition last:border-0 hover:bg-white/[0.03]"
        >
          <td
            v-for="col in columns"
            :key="col.name"
            class="max-w-xs px-4 py-2.5 align-top text-slate-300"
          >
            <a
              v-if="col.type === 'url' && row[col.i]"
              :href="asHref(row[col.i])"
              target="_blank"
              rel="noopener noreferrer"
              class="text-sky-400 hover:underline"
            >{{ row[col.i] }}</a>
            <Chip v-else-if="col.type === 'categorical' && row[col.i]" :value="row[col.i]" />
            <span
              v-else-if="col.type === 'long_text'"
              class="line-clamp-2 block w-72 whitespace-normal text-slate-400"
              :title="row[col.i]"
            >{{ row[col.i] }}</span>
            <span v-else-if="col.type === 'year' || col.type === 'number'" class="font-mono">{{ row[col.i] }}</span>
            <span v-else>{{ row[col.i] }}</span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
