<script setup lang="ts">
import { useProgress } from '../progress'

const props = defineProps<{ id: string; label?: string }>()
const { isComplete, toggle } = useProgress(props.id)
</script>

<template>
  <button class="progress-toggle" :class="{ complete: isComplete }" type="button" @click="toggle">
    <span aria-hidden="true">{{ isComplete ? '✓' : '○' }}</span>
    {{ isComplete ? '已完成' : (label || '标记完成') }}
  </button>
</template>

