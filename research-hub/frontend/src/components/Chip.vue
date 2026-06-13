<script setup>
import { chipClass } from '../lib/dataset'
defineProps({ value: { type: String, required: true } })
</script>

<template>
  <span
    class="inline-flex max-w-full items-center truncate rounded-full px-2.5 py-0.5 text-[11px] font-medium ring-1"
    :class="chipClass(value)"
  >{{ value }}</span>
</template>
